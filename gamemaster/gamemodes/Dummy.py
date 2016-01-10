import lib.Target
import gamemodes
from lib.CountdownTimer import CountdownTimer

## A dummy target that switches to green when hit
class Target(lib.Target.Target):
	def __init__(self,groupID,gameModeMaster,id,targetZIndex):
		lib.Target.Target.__init__(self,groupID,id,targetZIndex)
		print(self.__dict__)
		self.setColor("0000FF")
	
	def Hit(self,event):
		print("dummy target Hit()")
		print(event)
		self.setColor("00FF00")
	
	def Update(self,dt):
		"""Do game mode specific stuff."""
		pass

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gameInfo,gameEngine):
		gamemodes.Gamemode.__init__(self,gameInfo["duration"],gameEngine)
		self.players=players
		self.EffectCountdown=CountdownTimer(lambda: self.gameEngine.Effect("makeTargetRed"),2.0)

	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput=""
		main_score=[0 for i in range(len(self.players))]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}
	
	def InitializeTargets(self,hwTargets):
		targets=[]
		return targets
	
	def Update(self,dt):
		gamemodes.Gamemode.Update(self,dt)
		self.EffectCountdown.Update(dt)

def GetClasses():
	return {"targetClass":Target,"masterClass":Gamemode}
