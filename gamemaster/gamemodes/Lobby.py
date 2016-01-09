import lib.Target
import gamemodes

## A dummy target that switches to green when hit
class Target(lib.Target.Target):
	def __init__(self,group,gameWorld,id,targetZIndex):
		lib.Target.Target.__init__(self,group,gameWorld,id,targetZIndex)
	
	def Hit(self,event):
		pass
	
	def Update(self,dt):
		"""Do game mode specific stuff."""
		# TODO: lobby blinking

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gamestartInfo):
		pass

	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput="lobby"
		main_score=[]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}
	
	def Update(self,dt):
		pass


def GetClasses():
	"""Returns a tuple of classes for this game mode: (target,gameworld)"""
	return (Target,Gamemode)
