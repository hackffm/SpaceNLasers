from Target import Target

class TargetGroup:

	def __init__(self,gameWorld,targetGroupID,targetGroupZIndex):
		self.targetGroupID = ''
		self.targetGtoupZindex = -1
		self.gameWorld = None
		self.targetsList = []
		self.gameWorld = gameWorld
		self.targetGroupID = targetGroupID
		self.targetGroupZIndex = targetGroupZIndex

	def AddTarget(self,targetID,targetZIndex):
		self.targetsList.append(Target(self,self.gameWorld,targetID,targetZIndex))


	def CollectSerialBufferFromTargetsAsList(self):
		self.collectedSerialStringList = []
		for CSBFT_currentTarget in self.targetsList:
			self.currentTargetBuffer = CSBFT_currentTarget.CollectSerialBuffer()
			if self.currentTargetBuffer != '':
				self.collectedString = self.currentTargetBuffer
				self.collectedSerialStringList.append(self.collectedString)

		return self.collectedSerialStringList

	def UpdateTargets(self):
		for currentTarget in self.targetsList:
			currentTarget.Update()

	def GetTargetByID(self,GTBI_id):
		self.GTBI_found = None
		for GTBI_currentTarget in self.targetsList:
			if GTBI_currentTarget.targetID==GTBI_id:
				self.GTBI_found = GTBI_currentTarget
		return self.GTBI_found

	