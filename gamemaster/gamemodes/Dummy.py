import lib.Target

class Target(lib.Target.Target):
	"""A dummy target that really does nothing."""
	def __init__(self,group,gameWorld,id,targetZIndex):
		lib.Target.Target.__init__(self,group,gameWorld,id,targetZIndex)
	def Hit(self,event):
		"""Called from game engine when this target has been hit."""
		print(event)
		self.setColor("00FF00")
	def Update(self):
		"""Do game mode specific stuff."""
		pass

def GetClasses():
	"""Returns a tuple of classes for this game mode: (target,gameworld)"""
	return (Target,None)
