from TargetGroup import TargetGroup

class GameWorld:
	"""Helper functions for bus queries"""
	def __init__(self):
		self.targetCount = 0
		self.targetGroupList = []
		self.laserWeaponsList = []
		self.sounds = None
		self.eventList=[]



	def AddTargetGroup(self,targetGroupID,targetGroupZIndex):
		self.targetGroupList.append(TargetGroup(self,targetGroupID,targetGroupZIndex))

	def AddLaserWeapon(self,laserWeapon):
		self.laserWeaponsList.append(laserWeapon)


	def CollectTargetSerialBuffersAsList(self):
		self.collectedSerialBufferList = []
		for CTSBAL_currentTargetGroup in self.targetGroupList:
			self.collectedSerialBufferList+=CTSBAL_currentTargetGroup.CollectSerialBufferFromTargetsAsList()

		return self.collectedSerialBufferList

	def UpdateTargets(self):
		for UT_currentTargetGroup in self.targetGroupList:
			UT_currentTargetGroup.UpdateTargets()

	def GetTargetGroupByID(self,targetGroupID):
		GTGBID_found = None
		for GTGBID_currentTargetGroup in self.targetGroupList:
			if GTGBID_currentTargetGroup.targetGroupID==targetGroupID:
				GTGBID_found = GTGBID_currentTargetGroup
		return GTGBID_found
