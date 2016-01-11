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
	
	def _InitHardware(self,config):
		self.targetGroups={str(tg["id"]):[TargetInfo(str(t["id"]),int(t["zIndex"])) for t in tg["targets"]] for tg in config["targetControllers"]}
		self.weapons=[Weapon(str(w["code"]),int(w["shotCode"])) for w in config["weaponControllers"]]
		self.effects={str(name):str(command) for name,command in config["globalEffects"].iteritems()}
	
	def Effect(self,name):
		command=self.effects[name]
		print("global effect: {} -> command={}".format(name,command))
		self.gameHotLine.Ping(command)

	def LogEvent(self,event):
		self.eventLog.append(event)
		print(event)

	def Run(self):
		lobbydef={"game":{"mode":"lobby","duration":None},"players":[]}
		print("starting lobby...")
		gamestart=self.RunGame(lobbydef,lobbymode=True)
		print("starting game...")
		self.RunGame(gamestart)

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

	def DecodeHit(self,hitCode,weapon):
		if len(hitCode)<12:
			return []
		try:
			return [str(i) for i in range(6) if int(eval("0x"+hitCode[i*2:(i+1)*2]))==weapon.shotCode]
		except Exception as e:
			print("Decode hit error. Code: {} Error: {} ".format(hitCode,e))
			return []

	def PlaySoundAndWait(self,sound,wait):
		self.sounds[sound].play()
		time.sleep(wait)
	
	def _turnOnLaserWeapons(self):
		self.gameHotLine.Ping('AA102FF\n') # turn on Laserweapon A laser
		self.gameHotLine.Ping('BA102FF\n') # turn on Laserweapon B laser

	def _gameStart(self):
		self.gameHotLine.Ping('4A120FF040404\n') # blitz kommando
		self.gameHotLine.Ping('1A120FF040a2A\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]
		self.PlaySoundAndWait("boing8bitSound",1.5)
		self.PlaySoundAndWait("startSound",0.0)
		self.PlaySoundAndWait("musicSound",0.0)

		self._turnOnLaserWeapons()
	
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
	
	def _pollTargetHits(self,targets):
		for targetGroupID in self.targetGroups.keys():
			hitRaw = self.gameHotLine.PingPong(BusFactory.pollTargetState(targetGroupID)) # get target status
			for weapon in self.weapons:
				hitList = self.DecodeHit(hitRaw,weapon)
				for targetID in hitList:
					targetObj = targets[(targetGroupID,targetID)]
					event=Events.TargetHitEvent(time.time(),weapon,targetObj)
					targetObj.Hit(event)
					self.LogEvent(event)

