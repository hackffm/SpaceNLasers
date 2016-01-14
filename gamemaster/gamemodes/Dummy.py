import baseclasses
import lib.Target
from lib.CountdownTimer import CountdownTimer

## A dummy target that switches to green when hit
class Target(lib.Target.Target):
	def __init__(self, hwTarget, gameModeMaster):
		lib.Target.Target.__init__(self, hwTarget)
		print(self.__dict__)
		self.SetColor("0000FF")

	def Hit(self, event):
		lib.Target.Target.Hit(self, event)
		print("dummy target Hit()")
		print(event)
		self.SetColor("00FF00")

	def Update(self, dt):
		"""Do game mode specific stuff."""
		pass

class Gamemode(baseclasses.Gamemode):
	def __init__(self, players, gameInfo, gameEngine):
		baseclasses.Gamemode.__init__(self, gameInfo["duration"], gameEngine)
		self.players = players
		self.effectCountdown = CountdownTimer(lambda: self.gameEngine.Effect("makeTargetRed"), 2.0)

	def GetGameInfo(self, additionalConsoleOutput=""):
		myConsoleOutput = ""
		mainScore = [0]*len(self.players)
		return {"scores":{"score":{"type":"int", "values":mainScore}}, "consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}

	def InitializeTargets(self, hwTargets):
		targets = []
		return targets

	def Update(self, dt):
		baseclasses.Gamemode.Update(self, dt)
		self.effectCountdown.Update(dt)

def GetClasses():
	return {"targetClass":Target, "masterClass":Gamemode}
