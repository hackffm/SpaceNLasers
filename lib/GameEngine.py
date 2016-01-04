import time

from TimeCounter import TimeCounter
from random import randint


class GameEngine:

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

	def MainLoop(self):
		while 1:
			self.loops[self.gameState]()
			self.gameScreen.update()


	def LoopIntro(self):
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



	def GameStart(self):
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
		self.TurnOffAllTargets()
		self.GetRandomTarget(None).HitMe()
		self.currentActiveTarget = None
		self.gamePlatTimeCounter_TargetNext = time.time()+self.gamePlayTime_TargetLimit



	def LoopGamePlay(self):
		time.sleep(0.01)

		self.GameTargetContoller()

		if self.gamePlatTimeCounter_TargetNext<time.time():
			self.TurnOffAllTargets()
			self.gamePlatTimeCounter_TargetNext = time.time()+self.gamePlayTime_TargetLimit
			nextTarget = self.GetRandomTarget(self.currentActiveTarget)
			print "next Target: "+nextTarget.targetLEDAniHeader
			nextTarget.HitMe()
			self.currentActiveTarget = nextTarget

		# check game over timeout
		if self.gamePlayGameOverTimer.checkTimeout()==1:
			self.gameState = 'gameOver'
			return None
		
		a = self.gameHotLine.PingPong('Ab\n')
		self.gameWorld.UpdateTargets()
		self.PollTargetBuffer()
		if len(a)>=4:
			# print "weapon raw: "+a
			try:
				b=int(eval("0x"+a[0:2]))
			except:
				print "weapon button error: "+a
				b = 0
			
			if b == 2:
				self.laserAShrotGunMode = 1
			if b&1:

				# print a
				# print b
				# print bin(int(a, 16))[2:]

				# begin: laser shoot
				#self.gameHotLine.Ping('sB\n') # broadcast: ready to shoot weapon B
				self.gameHotLine.Ping('AA011FF000401\n')
				self.gameHotLine.Ping('Aa00704\n')
				self.gameHotLine.Ping('sA\n') # broadcast: ready to shoot weapon A
				time.sleep(0.01)
				self.gameHotLine.PingPong('S\n') # boradcast: shoot
				time.sleep(0.01)
				# end: laser shoot

				# print self.gameHotLine.PingPong('3t0\n') # debug target group


				
				self.gameWorld.sounds["laserblasterSound"].play()

				self.gameScreen.changeScore(25)
				

				self.laserAShrotGunMode = 0

				for currentTargetGroupA in self.gameWorld.targetGroupList:
					# print "hitRaw = self.gameHotLine.PingPong(currentTargetGroupA.targetGroupID)" + currentTargetGroupA.targetGroupID
					hitRaw = self.gameHotLine.PingPong(currentTargetGroupA.targetGroupID+'tr\n') # get target status
					time.sleep(0.01)	

					hitList = self.DecodeHit(hitRaw)	
					for LoopGamePlay_targetID in hitList:
						print 'target hit: '+currentTargetGroupA.targetGroupID+' - '+LoopGamePlay_targetID 
						self.playScore = self.playScore + 10
						
						TargetGroupObject = self.gameWorld.GetTargetGroupByID(currentTargetGroupA.targetGroupID)
						print "TargetGroupObject ID: "+TargetGroupObject.targetGroupID
						TargetObj = TargetGroupObject.GetTargetByID(LoopGamePlay_targetID)
						if TargetObj!=None:
							print "TargetObj ID: "+TargetObj.targetID
							if TargetObj.targetState == 'hitme':

								# update hit point on game screen
								self.gameScreen.show('Score') 
								#self.gameScreen.scorePlayer1=XXXX
								#self.gameScreen.scorePlayer2=XXXX
								self.gameScreen.update()

								# begin: next target
								nextTarget = self.GetRandomTarget(TargetObj)
								nextTarget.HitMe()
								print "next Target: "+nextTarget.targetLEDAniHeader
								self.currentActiveTarget = nextTarget
								# end: next target

								TargetObj.AddHit(self.gameWorld.laserWeaponsList[0],5,'laser')

								self.gameScreen.changeScore(25)

								if currentTargetGroupA.targetGroupID=='1' and LoopGamePlay_targetID=='1':
									# laser special effect on
									self.gameHotLine.Ping('1A120FF040a08\n')

	def DecodeHit(self,hitCode):
		hitSensor = []
		#print("hitCode",hitCode)
		try:
			if len(hitCode)>10:
				if int(eval("0x"+hitCode[0:2]))==145: # ==145
					print("hitCode[0:2]",int(eval("0x"+hitCode[0:2])))
					hitSensor.append('0')
				if int(eval("0x"+hitCode[2:4]))==145:
					print("hitCode[2:4]",int(eval("0x"+hitCode[2:4])))
					hitSensor.append('1')
				if int(eval("0x"+hitCode[4:6]))==145:
					print("hitCode[4:6]",int(eval("0x"+hitCode[4:6])))
					hitSensor.append('2')
				if int(eval("0x"+hitCode[6:8]))==145:
					print("hitCode[6:8]",int(eval("0x"+hitCode[6:8])))
					hitSensor.append('3')
				if int(eval("0x"+hitCode[8:10]))==145:
					print("hitCode[8:10]",int(eval("0x"+hitCode[8:10])))
					hitSensor.append('4')
				if int(eval("0x"+hitCode[10:12]))==145:
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
				print "theader: "+GRT_currentTarget.targetLEDAniHeader
				if GRT_currentTarget!=excludeTarget:
					allTargets.append(GRT_currentTarget)
		
		rID = randint(0,len(allTargets)-1)
		print "rID: "+str(rID)
		return allTargets[rID]


	def GameTargetContoller(self):
		return None

	def GameOver(self):
		self.gameScreen.pushCurrentScoreToHighScore()
		self.TurnOffAllTargets()
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


	def TurnOffAllTargets(self):
		for TOAT_currentTargetGroup in self.gameWorld.targetGroupList:
			for TOAT_currentTarget in TOAT_currentTargetGroup.targetsList:
				TOAT_currentTarget.TurnOffTarget()
		self.PollTargetBuffer()

	def HitMeAllTargets(self):
		for HMAT_currentTargetGroup in self.gameWorld.targetGroupList:
			for HMAT_currentTarget in HMAT_currentTargetGroup.targetsList:
				HMAT_currentTarget.HitMe()
		self.PollTargetBuffer()
	
		

	def PollTargetBuffer(self):
		targetSerialBufferAsList = self.gameWorld.CollectTargetSerialBuffersAsList()
		for targetGroup in targetSerialBufferAsList:
			for targetBuffer in targetGroup:
				print targetBuffer
				# time.sleep(0.001)
				self.gameHotLine.Ping(targetBuffer)
