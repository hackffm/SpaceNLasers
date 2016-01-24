import random
from colorsys import hsv_to_rgb

import baseclasses
from lib.CountdownTimer import CountdownTimer
from lib.hexstring import Myhex
import lib.Target

## Target which changes color randomly
class Target(lib.Target.Target):
	def __init__(self, hwTarget, gameModeMaster):
		lib.Target.Target.__init__(self, hwTarget)
		self.gameModeMaster = gameModeMaster
		self._ChangeColor() # change color on init because the countdown timer is initialised there

	def Hit(self, event):
		pass

	def Update(self, dt):
		self.countdownTimer.Update(dt)

	def _ChangeColor(self):
		hue = random.random()
		rgb = hsv_to_rgb(hue, 1.0, 1.0)
		colorstring = "".join([Myhex(int(rgb[i]*255)) for i in range(3)])
		self.SetColor(colorstring)
		self.countdownTimer = CountdownTimer(self._ChangeColor, random.uniform(0.8, 1.2))


class Gamemode(baseclasses.Gamemode):
	def __init__(self, players, gamestartInfo, gameEngine):
		pass

	def GetGameInfo(self, additionalConsoleOutput=""):
		myConsoleOutput = "Waiting for game start..."
		mainScore = []
		return {"scores":{"score":{"type":"int", "values":mainScore}}, "consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}

	def Update(self, dt):
		pass


def GetClasses():
	return {"targetClass":Target, "masterClass":Gamemode}
