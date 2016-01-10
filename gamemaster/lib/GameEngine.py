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
	def __init__(self,gameHotLine, gameScreen, sounds, runWithoutMenugod=True):
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
		# TODO: show events on screen/debug

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

class GameEngine2:

	def __init__(self,gameHotLine, gameWorld, gameScreen):
		self.gamePlayTime = 50
		self.gamePlayTime_TargetLimit = 3
		self.gamePlatTimeCounter_TargetNext = 0
		self.gameState = 'intro'
		self.gameHotLine = None
		self.gameWorld = None
		self.gameScreen = None
		self.loops = None
		self.introTimeCounter = None
		self.gamePlayGameOverTimer = None
		self.playScore = 0
		self.laserAShrotGunMode = 0

		self.gameHotLine = gameHotLine
		self.gameWorld = gameWorld
		self.gameScreen = gameScreen
		self.loops = {
		"intro": self.LoopIntro, 
		"gamestart": self.GameStart, 
		"gameOver": self.GameOver, 
		"LoopGamePlay": self.LoopGamePlay  }
		self.gamePlayGameOverTimer = TimeCounter()
		self.eventLog=[]
	
	def LogEvent(self,event):
		self.eventLog.append(event)
		print(event)
		# TODO: show events on screen/debug

	## calls other loops depending on state. only called once
	def MainLoop(self):
		while 1:
			self.loops[self.gameState]()
			self.gameScreen.update()
	
	def LoopIntro(self):
		"""waiting for game start. do lobby light show and sound FX"""
		if self.introTimeCounter==None:
			self.introTimeCounter = TimeCounter()

		if self.introTimeCounter.checkTimeout()==1:
			self.introTimeCounter.setTimeout(30)
			self.gameScreen.show('Start')
			self.gameHotLine.Ping('4A120FF04041A\n') # blitz kommando
			self.gameHotLine.Ping('1A020FF040a20\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]
			self.gameWorld.sounds["introSound"].play()

		time.sleep(0.01)
		a = self.gameHotLine.PingPong('Ab\n')
		if len(a)>=2:

			try:
				b=int(eval("0x"+a[0:2]))
			except:
				print "intro button error: "+a
				b = 0

			
			if b&4:
				self.gameWorld.sounds["mixer"].fadeout(200)
				time.sleep(0.2)
				self.gameState = 'gamestart'
		self.gameState="gamestart" # TODO: remove after testing


	def GameStart(self):
		"""Do transition from lobby to game mode light show and sound FX"""
		self.eventLoop=[]
		self.gameScreen.resetScore()
		self.gameHotLine.Ping('4A120FF040404\n') # blitz kommando
		self.gameHotLine.Ping('1A120FF040a2A\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]
		self.gameWorld.sounds["boing8bitSound"].play()
		self.gameScreen.show('Transition')
		time.sleep(1.5)
		self.gameWorld.sounds["startSound"].play()
		# time.sleep(10)
		print "Start Game"
		self.gameHotLine.Ping('AA102FF\n') # turn on Laserweapon A laser
		self.gameHotLine.Ping('BA102FF\n') # turn on Laserweapon B laser
		self.gameWorld.sounds["musicSound"].play()
		self.gameState = 'LoopGamePlay'
		self.gamePlayGameOverTimer.setTimeout(self.gamePlayTime)
		self.gameScreen.show('Score')
		# self.HitMeAllTargets()
		#self.TurnOffAllTargets()
		#self.GetRandomTarget(None).HitMe()
		self.currentActiveTarget = None
		self.gamePlatTimeCounter_TargetNext = time.time()+self.gamePlayTime_TargetLimit



	def LoopGamePlay(self):
		time.sleep(0.01)

		self.GameTargetContoller()

		#if self.gamePlatTimeCounter_TargetNext<time.time():
			#self.TurnOffAllTargets()
			#self.gamePlatTimeCounter_TargetNext = time.time()+self.gamePlayTime_TargetLimit
			#nextTarget = self.GetRandomTarget(self.currentActiveTarget)
			#print "next Target: "+nextTarget.targetLEDAniHeader
			#nextTarget.HitMe()
			#self.currentActiveTarget = nextTarget

		# check game over timeout
		if self.gamePlayGameOverTimer.checkTimeout()==1:
			self.gameState = 'gameOver'
			return None
		
		a = self.gameHotLine.PingPong('Ab\n') # requesting weapon status from weapon "A". returns 8 bit button and barrelcount data. 
		# detailed documentation check wiki, http://www.hackerspace-ffm.de/wiki/index.php?title=SpaceInLasers#Serielle_Kommandos
		# Section "Unicast Kommandos" -> "_b"
		# TODO: should poll all connected weapons on the game bus.

		self.gameWorld.UpdateTargets() # call target update method

		self.PollTargetBuffer() # collect from all targets serial bus data to required to be sent

		if len(a)>=4: # expecting four chars from weapon status 
			# print "weapon raw: "+a
			try:
				b=int(eval("0x"+a[0:2])) # try to convert first two chars to interger value
			except:
				print "weapon button error: "+a
				b = 0 # prevent do crap if crap data recieved
			
			if b == 2:
				self.laserAShrotGunMode = 1 # ?????
			if b&1: # default gun trigger pulled. next start laser shot sequence.

				# print a
				# print b
				# print bin(int(a, 16))[2:]

				# begin: shoot laser
				#self.gameHotLine.Ping('sB\n') # broadcast: ready to shoot weapon B
				self.gameHotLine.Ping('AA011FF000401\n') # weapon A "Rumble Shot" animation
				self.gameHotLine.Ping('Aa00704\n') # weapon A Neopixel animation ????? Do some blink blink ??!!
				self.gameHotLine.Ping('sA\n') # broadcast: ready to shoot weapon A for multiple weapon shot, for example weapon A and B send "sAB"
				time.sleep(0.01)
				self.gameHotLine.PingPong('S\n') # boradcast shoot. weapons fires 9 bit weapon id with the laser. targets pause any tasks, waiting for laser bit data.
				time.sleep(0.01)
				# end: laser shoot

				# print self.gameHotLine.PingPong('3t0\n') # debug target group

				self.gameWorld.sounds["laserblasterSound"].play()

				self.gameScreen.changeScore(25) # wtf?!
				

				self.laserAShrotGunMode = 0

				for currentTargetGroupA in self.gameWorld.targetGroupList:
					# print "hitRaw = self.gameHotLine.PingPong(currentTargetGroupA.targetGroupID)" + currentTargetGroupA.targetGroupID
					hitRaw = self.gameHotLine.PingPong(currentTargetGroupA.targetGroupID+'tr\n') # get target status. return value: AABBCCDDEEFFGGHH = data value
					time.sleep(0.01)	

					hitList = self.DecodeHit(hitRaw)	# decode recieved target hit status
					for LoopGamePlay_targetID in hitList:
						targetObj = currentTargetGroupA.GetTargetByID(LoopGamePlay_targetID)
						event=Events.TargetHitEvent(time.time(),self.gameWorld.laserWeaponsList[0],targetObj) # TODO: pass correct weapon from bus data
						targetObj.Hit(event)
						self.LogEvent(event)

	def GameOver(self):
		"""Game is over. Turn off weapons, do game over lightshow and sound FX"""
		self.gameScreen.pushCurrentScoreToHighScore()
		#self.TurnOffAllTargets()
		self.gameHotLine.Ping('AA10200\n') # trune off laser weapon A
		self.gameHotLine.Ping('BA10200\n') # trune off laser weapon B
		self.gameWorld.sounds["mixer"].fadeout(500) # stop all sounds
		time.sleep(0.5)

		self.gameScreen.show('GameOver')
		self.gameScreen.update()

		print "Game Over"
		self.gameWorld.sounds["gameOverSound"].play()
		time.sleep(4)
		self.gameScreen.show('Highscore')
		self.gameScreen.update()
		self.gameWorld.sounds["gameOverJingleSound"].play()
		time.sleep(7)
		self.gameState = 'intro'
		self.playScore = 0

	def DecodeHit(self,hitCode):
		"""try to decode hitCode AABBCCDDEEFFGGHH. for example AA contains hit data"""
		hitSensor = []
		#print("hitCode",hitCode)
		try:
			if len(hitCode)>10:
				if int(eval("0x"+hitCode[0:2]))==145:	# 0x91 or in binary 1001 0001
					print("hitCode[0:2]",int(eval("0x"+hitCode[0:2])))
					hitSensor.append('0')
				if int(eval("0x"+hitCode[2:4]))==145:  # 0x91 or in binary 1001 0001
					print("hitCode[2:4]",int(eval("0x"+hitCode[2:4])))
					hitSensor.append('1')
				if int(eval("0x"+hitCode[4:6]))==145:  # 0x91 or in binary 1001 0001
					print("hitCode[4:6]",int(eval("0x"+hitCode[4:6])))
					hitSensor.append('2')
				if int(eval("0x"+hitCode[6:8]))==145:  # 0x91 or in binary 1001 0001
					print("hitCode[6:8]",int(eval("0x"+hitCode[6:8])))
					hitSensor.append('3')
				if int(eval("0x"+hitCode[8:10]))==145:  # 0x91 or in binary 1001 0001
					print("hitCode[8:10]",int(eval("0x"+hitCode[8:10])))
					hitSensor.append('4')
				if int(eval("0x"+hitCode[10:12]))==145:  # 0x91 or in binary 1001 0001
					print("hitCode[10:12]",int(eval("0x"+hitCode[10:12])))
					hitSensor.append('5')
		except:
			print "Decode hit error: "+hitCode

		if len(hitSensor)>0:
			print("hitCode",hitCode)
		return hitSensor

	def GetRandomTarget(self,excludeTarget):
		allTargets = []
		print "allTargets:"
		for GRT_currentTargetGroup in self.gameWorld.targetGroupList:
			for GRT_currentTarget in GRT_currentTargetGroup.targetsList:
				if GRT_currentTarget!=excludeTarget:
					allTargets.append(GRT_currentTarget)
		
		rID = randint(0,len(allTargets)-1)
		print "rID: "+str(rID)
		return allTargets[rID]


	def GameTargetContoller(self):
		return None
		

	def PollTargetBuffer(self):
		targetSerialBufferAsList = self.gameWorld.CollectTargetSerialBuffersAsList()
		for targetGroup in targetSerialBufferAsList:
			for targetBuffer in targetGroup:
				print targetBuffer
				# time.sleep(0.001)
				self.gameHotLine.Ping(targetBuffer)
