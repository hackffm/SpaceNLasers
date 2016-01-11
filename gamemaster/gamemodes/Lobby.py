import lib.Target
import gamemodes
import random
from lib.CountdownTimer import CountdownTimer
from lib.hexstring import myhex

## Target which changes color randomly
class Target(lib.Target.Target):
	def __init__(self,hwTarget,gameModeMaster):
		lib.Target.Target.__init__(self,hwTarget)
		self.gameModeMaster=gameModeMaster
		self._changeColor() # change color on init because the countdown timer is initialised there
	
	def Hit(self,event):
		pass
	
	def Update(self,dt):
		self.countdownTimer.Update(dt)
	
	def _changeColor(self):
		r=random.randint(0,255)
		g=random.randint(0,255)
		b=random.randint(0,255)
		self.setColor(myhex(r)+myhex(g)+myhex(b))
		self.countdownTimer=CountdownTimer(self._changeColor,random.uniform(0.8,1.2))
		

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gamestartInfo,gameEngine):
		pass

	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput="Waiting for game start..."
		main_score=[]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}
	
	def Update(self,dt):
		pass


def GetClasses():
	return {"targetClass":Target,"masterClass":Gamemode}
