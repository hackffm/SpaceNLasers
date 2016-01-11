import time
import json

from HardwareTarget import HardwareTarget

from TimeCounter import TimeCounter
from random import randint
import Events
from MenuGod import MenuGod,AbortGameException,FakeMenuGod
import gamemodes
from Player import Player
import BusFactory
from Weapon import Weapon

class GameEngine:
	##
	# \param gameHotLine SerialHalfDuplex object for bus communication
	# \param sounds dictionary which maps sound names on sound files
	# \param hwconfig filename of hardware configuration
	# \param menugod which menugod host to connect to. empty string for server mode, None for testing FakeMenuGod
	# \param beamer similar connection for non-controlling connection. None disables beamer output
	def __init__(self,gameHotLine, sounds, hwconfig, menugod, beamer):
		self.gameHotLine=gameHotLine

		if beamer is None:
			self.beamer=FakeMenuGod()
		else:
			self.beamer=MenuGod(beamer)

		if menugod is None:
			self.menugod=FakeMenuGod()
		else:
			self.menugod=MenuGod(menugod)

		self.eventLog=[]
		self.sounds=sounds
		with open(hwconfig,"r") as fp:
			self._InitHardware(json.load(fp))

		print("initialising bus...")
		self.Effect("busInit")
	
	## Reads the hardware definitions (weapon/target controller codes etc.)
	def _InitHardware(self,config):
		self.weapons=[Weapon(str(w["code"]),int(w["shotCode"])) for w in config["weaponControllers"]]
		self.effects={str(name):str(command) for name,command in config["globalEffects"].iteritems()}
		self.hardwareTargets=[]
		self.targetGroupIDs=config["targetControllers"].keys()
		for groupID,groupDef in config["targetControllers"].iteritems():
			for target in groupDef["targets"]:
				self.hardwareTargets.append(HardwareTarget(groupID,target,self.globalConfig))
	
	## Starts a global effect
	# Global effects are: fog, stroboscope etc.
	def Effect(self,name):
		command=self.effects[name]
		print("global effect: {} -> command={}".format(name,command))
		self.gameHotLine.Ping(command)

	## Log an Event for later analysis 
	def LogEvent(self,event):
		self.eventLog.append(event)
		print(event)
	
	## Start the game engine and loop-run games started from MenuGod
	def Run(self):
		while(True):
			lobbydef={"game":{"mode":"lobby","duration":None},"players":[]}
			print("starting lobby...")
			gamestart=self.RunGame(lobbydef,lobbymode=True)
			print("starting game...")
			self.RunGame(gamestart)

	## Run a specific game
	# \param gamestart Dictionary as retrieved from MenuGod.CheckNewGameStart
	# \param lobbymode If set to True, a gamestart message will be expected from Menugod. If False (default), the game aborts on all messages received.
	def RunGame(self,gamestart,lobbymode=False):
		try:
			print("reading gamemode {}".format(gamestart["game"]["mode"]))
			gamemode_classes=gamemodes.available_modes[gamestart["game"]["mode"]]

			print("creating players...")
			self.players=[Player(p["name"],p["color"]) for p in gamestart["players"]]

			# TODO player<->weapon assignment
			for i in range(len(self.players)):
				self.weapons[i].player=self.players[i]

			print("creating game mode master...")
			self.gamemodeMaster=gamemode_classes["masterClass"](self.players,gamestart["game"],self)

			# initialize targets
			print("creating targets...")
			targets={
					gamemode_classes["targetClass"](hwTarget,self.gamemodeMaster)
					for hwTarget in self.hardwareTargets
				}
			self.gamemodeMaster.SetTargets(targets)

			if not lobbymode:
				self._gameStart()
			lastTime=time.time()
			print("starting game!")
			self.Effect("lobby" if lobbymode else "gameStart")
			while(True):
				now=time.time()
				dt=now-lastTime
				lastTime=now

				# main game logic
				self.gamemodeMaster.Update(dt)


				# target logic
				for t in targets:
					t.Update(dt)

				# weapons
				for weapon in self.weapons:
					code=self.gameHotLine.PingPong(BusFactory.getWeaponButtons(weapon.code))
					weapon.SetCurrentState(code)
					weapon.Update(dt)

				# start shoot sequence if trigger pulled
				self._shootSequence()

				# event logic
				self._pollTargetHits(targets)

				# menugod communication
				info=self.gamemodeMaster.getGameInfo()
				if lobbymode:
					gamestart=self.menugod.CheckNewGameStart()
					if gamestart:
						return gamestart
				else:
					self.menugod.SendGameInfo(info)
					self.beamer.SendGameInfo(info)

				# send target buffer
				for target in targets:
					for buf in target.CollectSerialBuffer():
						self.gameHotLine.Ping(buf)

		except gamemodes.GameOverException:
			self.menugod.GameOver()
			self.beamer.GameOver()
			self.Effect("gameOver")
			print("GAME OVER!")

		except AbortGameException:
			print("aborting game due to command from menugod")
	
	## Play a predefined sound and sleep
	# \param sound sound name to play. The sound has to be defined previously
	# \param time seconds to wait after play
	def PlaySoundAndWait(self,sound,wait):
		self.sounds[sound].play()
		time.sleep(wait)
	
	def _turnOnLaserWeapons(self):
		for weapon in self.weapons:
			self.gameHotLine.Ping(BusFactory.enableWeapon(weapon.code))
	
	## Game start sequence with lots of effects
	def _gameStart(self):
		self.Effect("gameIntro")
		self.PlaySoundAndWait("boing8bitSound",1.5)
		self.PlaySoundAndWait("startSound",0.0)
		self.PlaySoundAndWait("musicSound",0.0)

		self._turnOnLaserWeapons()
	
	## Start shooting sequence (disable lights, send laser info)
	# Hit data evaluation is done in _pollTargetHits to allow for delay in the targets
	def _shootSequence(self):
		shootingCodes=""
		for weapon in self.weapons:
			if weapon.ShootsThisFrame():
				shootingCodes+=weapon.code
				self.gameHotLine.Ping(BusFactory.rumbleShootAnimation(weapon.code))
				self.gameHotLine.Ping(BusFactory.doSomethingAnimationLikeOnWeapon(weapon.code))
		if len(shootingCodes)==0:
			return

		# begin: laser shoot
		self.gameHotLine.Ping(BusFactory.readyToShoot(shootingCodes))
		time.sleep(0.01)
		self.gameHotLine.PingPong(BusFactory.startShootingSequence())
		time.sleep(0.01)
		# end: laser shoot

		self.sounds["laserblasterSound"].play()
	
	## Retrieve hit data from all targets and start Target-specific processing
	# \param targets list of Target instances
	def _pollTargetHits(self,targets):
		for targetGroupID in self.targetGroupIDs:
			hitRaw = self.gameHotLine.PingPong(BusFactory.pollTargetState(targetGroupID)) # get target status
			for weapon in self.weapons:
				hitList = [str(i) for i in range(6) if int(eval("0x"+hitRaw[i*2:(i+1)*2]))==weapon.shotCode]
				for targetID in hitList:
					targetObj = [t for t in targets if t.hardwareTarget.id==targetID and t.hardwareTarget.groupID==targetGroupID][0]
					event=Events.TargetHitEvent(time.time(),weapon,targetObj)
					targetObj.Hit(event)
					self.LogEvent(event)

