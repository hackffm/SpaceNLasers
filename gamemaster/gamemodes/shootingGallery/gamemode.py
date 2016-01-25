import random

import gamemodes.baseclasses

from config import Config

class Gamemode(gamemodes.baseclasses.Gamemode):
	def __init__(self, players, gameInfo, gameEngine):
		gamemodes.baseclasses.Gamemode.__init__(self, gameInfo["duration"], gameEngine, players)
		self.players = players
		self.numOccupiedTargets = {p:0 for p in players}
		self.conf = Config()

	def AddPoint(self, player, value):
		self.scores[player] += value

	def GetGameInfo(self, additionalConsoleOutput=""):
		myConsoleOutput = ""
		mainScore = [int(self.scores[p]) for p in self.players]
		return {"scores":{"score":{"type":"int", "values":mainScore}}, "consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}

	def Update(self, dt):
		gamemodes.baseclasses.Gamemode.Update(self, dt)
		activeTargets = [t for t in self.targets if t.active]
		idleTargets = [t for t in self.targets if not t.active and t.owner is None]

		# make new active target
		newActiveProbability = (self.conf.maximumActiveTargets-len(activeTargets))*dt*self.conf.newTargetProbabilityModifier
		if random.random() < newActiveProbability and len(idleTargets) > 0:
			random.choice(idleTargets).Activate()

