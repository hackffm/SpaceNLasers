import time

from lib.TimeCounter import TimeCounter

class TargetHitRecord:
	

	def __init__(self,weapon,hitPoint,hitType):
		self.weapon = ''
		self.hitPoint = 5 # default hit point
		self.hitType = 'laser' # default hit type 
		self.weapon = weapon
		self.hitPoint = hitPoint
		self.hitType = hitType
		self.targetType = 'single'


class Target:

	

	def __init__(self,targetGroup,gameWorld,targetID,targetZIndex):
		self.targetLEDSerialCode_HitReady = '0200FFFF'
		self.targetLEDSerialCode_Hit = '02FF0000'
		self.targetLEDSerialCode_Off = '02000000'

		self.targetState = ''
		self.targetAnimationState = ''
		self.targetSerialBuffer = ''

		self.targetHitList = []

		self.targetLastHit = ''

		self.tickTock = 0

		self.targetSpecialSerialCommand = '' 

		self.animationTickTockNext = -1
		self.animationNextDo = ''
		self.gameWorld = None
		self.targetGroup = None


		self.gameWorld = gameWorld
		self.targetID = targetID
		self.targetZIndex = targetZIndex
		self.tickTock = time.time()
		self.targetGroup = targetGroup
		print "target.init self.targetGroup.targetGroupID: "+self.targetGroup.targetGroupID

		self.targetLEDAniHeader = self.targetGroup.targetGroupID+'a'+self.targetID
		print "target.init self.targetLEDAniHeader: "+self.targetLEDAniHeader
		# self.targetSerialBuffer = self.targetLEDAniHeader+self.targetLEDSerialCode_Off+'\n'
		self.targetSerialBuffer = ''

	def HitMe(self):
		self.targetState = 'hitme'
		self.targetSerialBuffer = self.targetLEDAniHeader+self.targetLEDSerialCode_HitReady+'\n'

	def AddHit(self,weapon,hitPoint,hitType):
		if self.targetState=='hitme':
			self.targetState = ''
			self.newHit = TargetHitRecord(weapon,hitPoint,hitType)
			self.targetLastHit = self.newHit
			# self.targetHitList.append(newHit)
			self.MakeHitSerialBuffer()
			self.animationTickTockNext = time.time()+1
			self.animationNextDo = 'TurnOffNeoPixel'
			self.gameWorld.sounds["explosionSound"].play()
			
		
	def MakeHitSerialBuffer(self):
		print 'MakeHitSerialBuffer hit: '+self.targetLEDAniHeader
		self.targetState = 'recieved hit'
		self.targetSerialBuffer = self.targetLEDAniHeader+self.targetLEDSerialCode_Hit+'\n'

	def CollectSerialBuffer(self):
		self.serialBuffer = self.targetSerialBuffer
		self.targetSerialBuffer = ''
		return self.serialBuffer

	def Update(self):
		self.tickTock = time.time()
		self.UpdateAnimation()


	def TurnOffTarget(self):
		self.targetSerialBuffer = self.targetLEDAniHeader+self.targetLEDSerialCode_Off+'\n'
		self.targetState = ''
		

	def UpdateAnimation(self):
		if self.animationTickTockNext!=-1:
			self.deltaTickTock = self.tickTock - self.animationTickTockNext
			self.deltaTickTockMiliseconds = self.deltaTickTock * 1000
			if self.deltaTickTockMiliseconds>0 and self.animationNextDo!='':
				if self.animationNextDo=='TurnOffNeoPixel':
					self.TurnOffNeoPixel()
				self.animationNextDo = ''
				self.animationTickTockNext = -1
				self.targetState=''


	def TurnOffNeoPixel(self):
		self.targetSerialBuffer = self.targetLEDAniHeader+self.targetLEDSerialCode_Off+'\n'

