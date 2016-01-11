import lib.Target
import gamemodes
import json

class Target(lib.Target.Target):
	def __init__(self,groupID,gameModeMaster,id,targetZIndex):
		lib.Target.Target.__init__(self,groupID,id,targetZIndex)
		self.protected=False
		self.owner=None
		self.gameModeMaster=gameModeMaster
		self.setColor("FFFFFF")
	
	def Hit(self,event):
		print("hit")
		if not self.protected:
			self.setOwner(event.weapon.player)

	def Update(self,dt):
		pass

	def setOwner(self,player):
		self.setColor(player.color)
		if self.owner is not None:
			self.gameModeMaster.numOccupiedTargets[self.owner]-=1
		if player is not None:
			self.gameModeMaster.numOccupiedTargets[player]+=1
		self.owner=player

class Gamemode(gamemodes.Gamemode):
	def __init__(self,players,gameInfo,gameEngine):
		gamemodes.Gamemode.__init__(self,gameInfo["duration"],gameEngine)
		self.players=players
		self.scores={p:0.0 for p in players}
		self.numOccupiedTargets={p:0 for p in players}
		with open("gamemodes/Domination.json","r") as fp:
			self.conf=json.load(fp)

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
			self.scores[p]+=self.numOccupiedTargets[p]*dt*self.conf["scoreFactor"]/self.duration



def GetClasses():
	return {"targetClass":Target,"masterClass":Gamemode}
