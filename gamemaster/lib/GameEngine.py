import time
import json

from HardwareTarget import HardwareTarget

import Events
from MenuGod import MenuGod, AbortGameException, FakeMenuGod
from Player import Player
import BusFactory
from Weapon import Weapon
from CountdownTimer import CountdownTimer
import gamemodes
from SoundManager import SoundManager
from DMXEffects import DMXEffectManager

class GameEngine(object):
	##
	# \param gameHotLine SerialHalfDuplex object for bus communication
	# \param hwconfig filename of hardware configuration
	# \param menugod which menugod host to connect to. empty string for server mode, None for testing FakeMenuGod
	# \param beamer similar connection for non-controlling connection. None disables beamer output
	def __init__(self, gameHotLine, hwconfig, menugod, beamer, dmxEffects):
		self.gameHotLine = gameHotLine
		self.busErrorLog = {}
		self.busErrorString = ""

		print("initialising sound system...")
		self.soundManager = SoundManager()
		self.sound = self.soundManager.sets[0]

		print("connecting to beamer...")
		if beamer is None:
			self.beamer = FakeMenuGod()
		else:
			self.beamer = MenuGod(beamer)

		print("connecting to menugod")
		if menugod is None:
			self.menugod = FakeMenuGod()
		else:
			self.menugod = MenuGod(menugod)

		self.eventLog = []

		print("loading hardware configuration...")
		with open("hardwareconfig/global.json", "r") as fp:
			self.globalConfig = json.load(fp)
		with open(hwconfig, "r") as fp:
			self.config = json.load(fp)

		self._InitHardware()

		self.dmxController = DMXEffectManager(dmxEffects, self.config["dmx"])

		print("initialising bus...")
		self.Effect("busInit")

	## Reads the hardware definitions (weapon/target controller codes etc.)
	def _InitHardware(self):
		self.weapons = [Weapon(str(w["code"]), int(w["shotCode"])) for w in self.config["weaponControllers"]]
		self.effects = {str(name):str(command) for name, command in self.config["globalEffects"].iteritems()}
		self.hardwareTargets = []
		self.targetGroupIDs = self.config["targetControllers"].keys()
		for groupID, groupDef in self.config["targetControllers"].iteritems():
			for target in groupDef["targets"]:
				self.hardwareTargets.append(HardwareTarget(groupID, target, self.globalConfig))

	## Starts a global effect
	# Global effects are: fog, stroboscope etc.
	def Effect(self, name):
		command = self.effects[name]
		print("global effect: {} -> command={}".format(name, command))
		self.gameHotLine.Ping(command)
		self.dmxController.Effect(name)

	## Log an Event for later analysis
	def LogEvent(self, event):
		self.eventLog.append(event)
		print(event)
	
	def AddBusError(self, e):
		print("new error: {}".format(e))

		if False: # raise all errors instead of logging
			if e.e is not None:
				raise e.e
			else:
				raise e

		if not e.source in self.busErrorLog:
			self.busErrorLog[e.source] = 0
		self.busErrorLog[e.source] += 1

		self.busErrorString = "current bus error statistic:\n" + "\n".join("{}: {}".format(source, count) for source, count in self.busErrorLog.iteritems())

	## Start the game engine and loop-run games started from MenuGod
	def Run(self):
		while(True):
			lobbydef = {"game":{"mode":"lobby", "duration":0}, "players":[]}
			print("starting lobby...")
			gamestart = self.RunGame(lobbydef, lobbymode=True)
			print("starting game...")
			self.RunGame(gamestart)

	## Run a specific game
	# \param gamestart Dictionary as retrieved from MenuGod.CheckNewGameStart
	# \param lobbymode If set to True, a gamestart message will be expected from Menugod. If False (default), the game aborts on all messages received.
	def RunGame(self, gamestart, lobbymode=False):
		try:
			soundSetNumber, musicNumber, duration = self.soundManager.GetDurations()[gamestart["game"]["duration"]]
			self.sound = self.soundManager.sets[soundSetNumber]
			duration -= self.sound.intro.get_length()
			gamestart["game"]["duration"] = duration # dirty hack!

			print("reading gamemode {}".format(gamestart["game"]["mode"]))
			gamemodeClasses = gamemodes.availableModes[gamestart["game"]["mode"]]

			print("creating players...")
			players = [Player(p["name"], p["color"]) for p in gamestart["players"]]

			# TODO player<->weapon assignment
			for i, player in enumerate(players):
				self.weapons[i].player = player

			print("creating game mode master...")
			gamemodeMaster = gamemodeClasses["masterClass"](players, gamestart["game"], self)

			# initialize targets
			print("creating targets...")
			targets = {
					gamemodeClasses["targetClass"](hwTarget, gamemodeMaster)
					for hwTarget in self.hardwareTargets
			}
			self._DisableAllTargets(targets)
			gamemodeMaster.SetTargets(targets)
			gamemodeMaster.Init()

			if not lobbymode:
				self.sound.mainMusics[musicNumber].play()
				self._GameStart()

			lastTime = time.time()
			print("starting game!")
			self.Effect("lobby" if lobbymode else "gameStart")
			while(True):
				now = time.time()
				dt = now-lastTime
				lastTime = now

				# main game logic
				gamemodeMaster.Update(dt)


				# target logic
				for target in targets:
					target.Update(dt)

				# weapons
				for weapon in self.weapons:
					try:
						code = self.gameHotLine.PingPong(BusFactory.GetWeaponButtons(weapon.code))
						weapon.SetCurrentState(code)
					except BusFactory.InvalidBusReply as e:
						self.AddBusError(e)
					weapon.Update(dt)

				# timer logic
				CountdownTimer.UpdateAll(dt)

				# start shoot sequence if trigger pulled
				self._ShootSequence()

				# event logic
				self._PollTargetHits(targets)

				# menugod communication
				info = gamemodeMaster.GetGameInfo()
				if lobbymode:
					gamestart = self.menugod.CheckNewGameStart()
					if gamestart:
						self.beamer.SendNewGameStart(gamestart)
						return gamestart
				else:
					self.beamer.SendGameInfo(info)
					info["consoleoutput"] += self.busErrorString
					self.menugod.SendGameInfo(info)

				# send target buffer
				self._SendTargetBuffers(targets)

		except gamemodes.baseclasses.GameOverException:
			self._DisableAllTargets(targets)
			self.menugod.GameOver()
			self.beamer.GameOver()
			self.Effect("gameOver")
			self.sound.PlayAndSleep("gameOver")
			print("GAME OVER!")

		except AbortGameException:
			self._DisableAllTargets(targets)
			print("aborting game due to command from menugod")
		finally:
			CountdownTimer.Clear()
			for m in self.sound.mainMusics:
				m.stop()
	

	def _SendTargetBuffers(self, targets):
		for target in targets:
			for buf in target.CollectSerialBuffer():
				self.gameHotLine.Ping(buf)


	def _TurnOnLaserWeapons(self):
		for weapon in self.weapons:
			self.gameHotLine.Ping(BusFactory.EnableWeapon(weapon.code))

	## Game start sequence with lots of effects
	def _GameStart(self):
		self.Effect("gameIntro")
		self.sound.intro.play()
		time.sleep(self.sound.intro.get_length())

		self._TurnOnLaserWeapons()

	def _DisableAllTargets(self, targets):
		for target in targets:
			target.Effect("disable")
		self._SendTargetBuffers(targets)

	## Start shooting sequence (disable lights, send laser info)
	# Hit data evaluation is done in _pollTargetHits to allow for delay in the targets
	def _ShootSequence(self):
		shootingCodes = ""
		for weapon in self.weapons:
			if weapon.ShootsThisFrame():
				shootingCodes += weapon.code
				self.gameHotLine.Ping(BusFactory.RumbleShootAnimation(weapon.code))
				self.gameHotLine.Ping(BusFactory.DoSomethingAnimationLikeOnWeapon(weapon.code))
		if len(shootingCodes) == 0:
			return

		# begin: laser shoot
		self.gameHotLine.Ping(BusFactory.ReadyToShoot(shootingCodes))
		time.sleep(0.01)
		self.gameHotLine.PingPong(BusFactory.StartShootingSequence()) # TODO why pong necessary?
		time.sleep(0.01)
		# end: laser shoot

		self.sound.laser.play()

	## Retrieve hit data from all targets and start Target-specific processing
	# \param targets list of Target instances
	def _PollTargetHits(self, targets):
		for targetGroupID in self.targetGroupIDs:
			try:
				hitRaw = self.gameHotLine.PingPong(BusFactory.PollTargetState(targetGroupID)) # get target status
				if len(hitRaw) < 12:
					raise BusFactory.InvalidBusReply(targetGroupID, None, "hitRaw response too short ({}): \"{}\"".format(len(hitRaw), hitRaw))
				for weapon in self.weapons:
					try:
						hitList = [str(i) for i in range(len(hitRaw)/2-1) if int(hitRaw[i*2:(i+1)*2], 16) == weapon.shotCode] # -2 because of \r\n
					except ValueError as e:
						raise BusFactory.InvalidBusReply(targetGroupID, e, str(e))
					for targetID in hitList:
						try:
							targetObj = [t for t in targets if t.hardwareTarget.id == targetID and t.hardwareTarget.groupID == targetGroupID][0]
						except IndexError as e:
							raise BusFactory.InvalidBusReply(targetGroupID, e, "invalid target number: {}".format(targetID))
						event = Events.TargetHitEvent(time.time(), weapon, targetObj)
						targetObj.Hit(event)
						self.LogEvent(event)
			except BusFactory.InvalidBusReply as e:
				self.AddBusError(e)

