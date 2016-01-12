import lib.Target
import gamemodes
import json
from lib.CountdownTimer import CountdownTimer
import random
from lib.Player import Player

class Target(lib.Target.Target):
	def __init__(self,hwTarget,gameModeMaster):
		lib.Target.Target.__init__(self,hwTarget)
		self.protectionTimer=CountdownTimer(lambda: None, 0.0)
		self.protected=False
		self.owner=None
		self.gameModeMaster=gameModeMaster
		self.active=False
		self.Effect("disable")
	
	def Activate(self):
		self.Effect("enable")
		self.active=True
	
	def Hit(self,event):
		if self.active:
			lib.Target.Target.Hit(self,event)
			if not self.protected:
				self.setOwner(event.weapon.player)

	def Update(self,dt):
		self.protectionTimer.Update(dt)
	
	def _unprotect(self):
		self.protected=False

	def setOwner(self,player):
		self.setColor(player.color)
		if self.owner is not None:
			self.gameModeMaster.occupiedArea[self.owner]-=self.hardwareTarget.scoreValue
		if player is not None:
			self.gameModeMaster.occupiedArea[player]+=self.hardwareTarget.scoreValue
			self.gameModeMaster.gameEngine.PlaySoundAndWait("targetDestroyed",0)
		self.protectionTimer=CountdownTimer(self._unprotect, self.gameModeMaster.conf["targetProtectionDuration"])
		self.protected=True
		self.owner=player

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gameInfo,gameEngine):
		gamemodes.Gamemode.__init__(self,gameInfo["duration"],gameEngine)
		self.players=players
		self.scores={p:0.0 for p in players}
		self.occupiedArea={p:0.0 for p in players}
		with open("gamemodes/Domination.json","r") as fp:
			self.conf=json.load(fp)
		CountdownTimer.Add(self._activateSimpleTarget, self.conf["newTargetTime"], loop=True)
		CountdownTimer.Add(self._activateVirobis, self.conf["buildupDuration"])
		CountdownTimer.Add(self._startEndgame, self.conf["endgameTime"])
		self.mode="buildup"
		self.alienFaction=Player("alien",self.conf["alienFactionColor"])
		self.occupiedArea[self.alienFaction]=0.0
	
	def Init(self):
		for i in range(self.conf["startupTargetCount"]):
			self._activateSimpleTarget()
	
	def _activateSimpleTarget(self):
		inactive_simple_targets=[target for target in self.targets if not target.active and target.hardwareTarget.type["group"]=="simple"]
		if len(inactive_simple_targets)>0:
			target=random.choice(inactive_simple_targets)
			target.Activate()
	
	def _activateVirobis(self):
		for target in self.targets:
			if target.hardwareTarget.type["group"]=="extra":
				target.Activate()	
	def _startEndgame(self):
		ms=self._getMothership()
		ms.Activate()
		ms.setOwner(self.alienFaction)
		CountdownTimer.Add(self._mothershipFire,self.conf["mothershipReload"],loop=True)


	def getGameInfo(self,additionalConsoleOutput=""):
		myConsoleOutput=""
		main_score=[int(self.scores[p]) for p in self.players]
		return {"scores":{"score":{"type":"int","values":main_score}},"consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}
	
	def InitializeTargets(self,hwTargets):
		targets=[]
		return targets
	
	def Update(self,dt):
		gamemodes.Gamemode.Update(self,dt)
		for p in self.players:
			self.scores[p]+=self.occupiedArea[p]*dt*self.conf["scoreFactor"]/self.duration
	
	def _getMothership(self):
		return [t for t in self.targets if t.hardwareTarget.type["group"]=="mothership"][0]

	
	def _mothershipFire(self):
		target=random.choice([t for t in self.targets if t.hardwareTarget.type["group"]=="simple"])
		if not target.protected:
			target.setOwner(self._getMothership().owner)


def GetClasses():
	return {"targetClass":Target,"masterClass":Gamemode}
