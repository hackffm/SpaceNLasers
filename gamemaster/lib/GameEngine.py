import time
import json

from TargetGroup import TargetInfo

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
	# \param runWithoutMenugod if True, a FakeMenuGod will be created to allow for testing without a MenuGod instance
	def __init__(self,gameHotLine, sounds, runWithoutMenugod=True):
		self.gameHotLine=gameHotLine
		if runWithoutMenugod:
			self.menugod=FakeMenuGod()
		else:
			self.menugod=MenuGod(None)
		self.eventLog=[]
		self.sounds=sounds
		with open("hardwareconfig/testbox.json","r") as fp:
			self._InitHardware(json.load(fp))
	
	## Reads the hardware definitions (weapon/target controller codes etc.)
	def _InitHardware(self,config):
		self.targetGroups={str(tg["id"]):[TargetInfo(str(t["id"]),int(t["zIndex"])) for t in tg["targets"]] for tg in config["targetControllers"]}
		self.weapons=[Weapon(str(w["code"]),int(w["shotCode"])) for w in config["weaponControllers"]]
		self.effects={str(name):str(command) for name,command in config["globalEffects"].iteritems()}
	
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
					(targetGroupID,target.targetID) : gamemode_classes["targetClass"](targetGroupID,self.gamemodeMaster,target.targetID,target.targetZIndex)
					for targetGroupID,targetGroup in self.targetGroups.iteritems()
					for target in targetGroup
				}

			if not lobbymode:
				self._gameStart()
			lastTime=time.time()
			print("starting game!")
			while(True):
				now=time.time()
				dt=now-lastTime
				lastTime=now

				# main game logic
				self.gamemodeMaster.Update(dt)


				# target logic
				for t in targets.values():
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

				# send target buffer
				for target in targets.values():
					for buf in target.CollectSerialBuffer():
						self.gameHotLine.Ping(buf)

		except gamemodes.GameOverException:
			self.menugod.GameOver()

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
		self.Effect("startupSequence")
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
		self.gameHotLine.PingPong('S\n') # boradcast: shoot
		time.sleep(0.01)
		# end: laser shoot

		self.sounds["laserblasterSound"].play()
	
	## Retrieve hit data from all targets and start Target-specific processing
	# \param targets list of Target instances
	def _pollTargetHits(self,targets):
		for targetGroupID in self.targetGroups.keys():
			hitRaw = self.gameHotLine.PingPong(BusFactory.pollTargetState(targetGroupID)) # get target status
			for weapon in self.weapons:
				hitList = [str(i) for i in range(6) if int(eval("0x"+hitCode[i*2:(i+1)*2]))==weapon.shotCode]
				for targetID in hitList:
					targetObj = targets[(targetGroupID,targetID)]
					event=Events.TargetHitEvent(time.time(),weapon,targetObj)
					targetObj.Hit(event)
					self.LogEvent(event)

