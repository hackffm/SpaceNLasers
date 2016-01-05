from gamemodes.Dummy import Target

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
		buf=[]
		for t in self.targetsList:
			buf+=t.CollectSerialBuffer()
		return buf

	def UpdateTargets(self):
		for currentTarget in self.targetsList:
			currentTarget.Update()

	def GetTargetByID(self,GTBI_id):
		self.GTBI_found = None
		for GTBI_currentTarget in self.targetsList:
			print(GTBI_currentTarget.targetID,GTBI_id)
			if GTBI_currentTarget.targetID==GTBI_id:
				self.GTBI_found = GTBI_currentTarget
		return self.GTBI_found

	
