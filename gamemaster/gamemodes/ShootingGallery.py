import lib.Target
import gamemodes
import json
import random
from lib.CountdownTimer import CountdownTimer

class Target(lib.Target.Target):
	def __init__(self,hwTarget,gameModeMaster):
		lib.Target.Target.__init__(self,hwTarget)
		self.gameModeMaster=gameModeMaster

		self.timeout=CountdownTimer(lambda: None, 0.0)

		self.Deactivate()
	
	def Activate(self):
		print("target activated")
		self.active=True
		self.Effect("enable")
		self.timeout=CountdownTimer(self.Deactivate, self.gameModeMaster.conf["activeTimeout"])
	
	def Deactivate(self):
		print("target deactivated")
		self.active=False
		self.owner=None
		self.Effect("disable")
	
	def Hit(self,event):
		lib.Target.Target.Hit(self,event)
		if self.active:
			print("hit!")
			self.gameModeMaster.gameEngine.PlaySoundAndWait("targetDestroyed",0)
			self.active=False
			self.owner=event.weapon.player
			self.setColor(event.weapon.player.color)
			self.timeout=CountdownTimer(self.Deactivate, self.gameModeMaster.conf["owningTime"])
			self.gameModeMaster.AddPoint(event.weapon.player, self.hardwareTarget.scoreValue)
	
	def Update(self,dt):
		self.timeout.Update(dt)

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gameInfo,gameEngine):
		gamemodes.Gamemode.__init__(self,gameInfo["duration"],gameEngine)
		self.players=players
		self.scores={p:0.0 for p in players}
		self.numOccupiedTargets={p:0 for p in players}
		with open("gamemodes/ShootingGallery.json","r") as fp:
			self.conf=json.load(fp)
	
	def AddPoint(self, player, value):
		self.scores[player]+=value

	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput=""
		main_score=[int(self.scores[p]) for p in self.players]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}

	def Update(self,dt):
		gamemodes.Gamemode.Update(self,dt)
		activeTargets=[t for t in self.targets if t.active]
		idleTargets=[t for t in self.targets if not t.active and t.owner is None]

		# make new active target
		newActiveProbability=(self.conf["maximumActiveTargets"]-len(activeTargets))*dt*self.conf["newTargetProbabilityModifier"]
		if random.random()<newActiveProbability and len(idleTargets)>0:
			random.choice(idleTargets).Activate()


def GetClasses():
	return {"targetClass":Target,"masterClass":Gamemode}
