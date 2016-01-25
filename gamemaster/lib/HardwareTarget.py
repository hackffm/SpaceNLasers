class HardwareTarget(object):
	def __init__(self, groupID, hwdef, globalConfig, localConfig):
		self.groupID = groupID
		self.id = hwdef["id"]
		self.zIndex = hwdef["zIndex"]
		self.scoreValue = hwdef["scoreValue"]
		self.type = globalConfig["targetTypes"][hwdef["type"]]
		self.effects = {eventName: localConfig["globalEffects"][effectName]
			for eventName,effectName in hwdef.iteritems()
			if eventName in ["enable","disable","hit","destroy"]}

	def GetEffect(self, name, *args):
		groupSpecificEffect = str(self.type["effects"][name].format(*args, targetGroup=self.groupID, targetID=self.id))
		targetSpecificEffect = self.effects[name] if name in self.effects else ""
		return targetSpecificEffect + groupSpecificEffect
