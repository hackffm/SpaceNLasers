import random

import gamemodes.baseclasses
from config import Config

from lib.Player import Player
from lib.CountdownTimer import CountdownTimer

class Gamemode(gamemodes.baseclasses.Gamemode):
	def __init__(self, players, gameInfo, gameEngine):
		gamemodes.baseclasses.Gamemode.__init__(self, gameInfo["duration"], gameEngine)
		self.players = players
		self.scores = {p:0.0 for p in players}
		self.occupiedArea = {p:0.0 for p in players}
		self.conf = Config()
		CountdownTimer.Add(self._ActivateSimpleTarget, self.conf.newTargetTime, loop=True)
		CountdownTimer.Add(self._ActivateVirobis, self.conf.buildupDuration)
		CountdownTimer.Add(self._StartEndgame, self.conf.endgameTime)
		self.mode = "buildup"
		self.alienFaction = Player("alien", self.conf.alienFactionColor)
		self.occupiedArea[self.alienFaction] = 0.0

	def Init(self):
		for _ in range(self.conf.startupTargetCount):
			self._ActivateSimpleTarget()

	def _ActivateSimpleTarget(self):
		inactiveSimpleTargets = [target for target in self.targets if not target.active and target.hardwareTarget.type["group"] == "simple"]
		if len(inactiveSimpleTargets) > 0:
			target = random.choice(inactiveSimpleTargets)
			target.Activate()

	def _ActivateVirobis(self):
		for target in self.targets:
			if target.hardwareTarget.type["group"] == "extra":
				target.Activate()

	def _StartEndgame(self):
		ms = self._GetMothership()
		ms.Activate()
		ms.SetOwner(self.alienFaction)
		CountdownTimer.Add(self._MothershipFire, self.conf.mothershipReload, loop=True)


	def GetGameInfo(self, additionalConsoleOutput=""):
		myConsoleOutput = ""
		mainScore = [int(self.scores[p]) for p in self.players]
		return {"scores":{"score":{"type":"int", "values":mainScore}}, "consoleoutput":myConsoleOutput+"\n"+additionalConsoleOutput}

	def InitializeTargets(self, hwTargets):
		targets = []
		return targets

	def Update(self, dt):
		gamemodes.baseclasses.Gamemode.Update(self, dt)
		for player in self.players:
			self.scores[player] += self.occupiedArea[player]*dt*self.conf.scoreFactor/self.duration

	def _GetMothership(self):
		return [t for t in self.targets if t.hardwareTarget.type["group"] == "mothership"][0]


	def _MothershipFire(self):
		target = random.choice([t for t in self.targets if t.hardwareTarget.type["group"] == "simple"])
		if not target.protected:
			target.SetOwner(self._GetMothership().owner)


