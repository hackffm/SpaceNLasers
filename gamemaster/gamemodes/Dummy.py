import lib.Target
import gamemodes

## A dummy target that switches to green when hit
class Target(lib.Target.Target):
	def __init__(self,group,gameWorld,id,targetZIndex):
		lib.Target.Target.__init__(self,group,gameWorld,id,targetZIndex)
		print(self.__dict__)
		self.setColor("FF0000")
	
	def Hit(self,event):
		print("dummy target Hit()")
		print(event)
		self.setColor("00FF00")
	
	def Update(self,dt):
		"""Do game mode specific stuff."""
		pass

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gameInfo):
		gamemodes.Gamemode.__init__(self,gameInfo["duration"])
		self.players=players

	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput=""
		main_score=[0 for i in range(len(self.players))]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}
	
	def InitializeTargets(self,hwTargets):
		targets=[]
		return targets
	
	def Update(self,dt):
		gamemodes.Gamemode.Update(self,dt)


def GetClasses():
	"""Returns a tuple of classes for this game mode: (target,gameworld)"""
	return (Target,Gamemode)
