class HardwareTarget:
	def __init__(self,groupID,hwdef,globalConfig):
		self.groupID=groupID
		self.id=hwdef["id"]
		self.zIndex=hwdef["zIndex"]
		self.type=globalConfig["targetTypes"][hwdef["type"]]
	
	def getEffect(self,name,*args):
		return self.type["effects"][name].format(*args,targetGroup=self.groupID, targetID=self.id)
