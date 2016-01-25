import random

import gamemodes.baseclasses
from config import Config

from lib.Player import Player
from lib.CountdownTimer import CountdownTimer

class Gamemode(gamemodes.baseclasses.Gamemode):
	def __init__(self, players, gameInfo, gameEngine):
		duration = gameInfo["duration"]
		gamemodes.baseclasses.Gamemode.__init__(self, duration, gameEngine)
		self.players = players
		self.scores = {p:0.0 for p in players}
		self.occupiedArea = {p:0.0 for p in players}
		self.conf = Config()
		CountdownTimer.Add(self._ActivateSimpleTarget, self.conf.newTargetTime, loop=True)
		CountdownTimer.Add(self._ActivateVirobis, self.conf.buildupDuration*duration)
		CountdownTimer.Add(self._StartEndgame, self.conf.endgameTime*duration)
		self.mode = "buildup"
		self.alienFaction = Player("alien", self.conf.alienFactionColor)
		self.occupiedArea[self.alienFaction] = 0.0

	def Init(self):
		self.totalArea=sum((target.hardwareTarget.scoreValue for target in self.targets))
		for _ in range(self.conf.startupTargetCount):
			self._ActivateSimpleTarget()

	def _ActivateSimpleTarget(self):
		inactiveSimpleTargets = [target for target in self.targets if not target.active and target.hardwareTarget.type["group"] == "simple"]
		if len(inactiveSimpleTargets) > 0:
			target = random.choice(inactiveSimpleTargets)
			target.Activate()
			target.SetColor(self.alienFaction.color)

	def _ActivateVirobis(self):
		for target in self.targets:
			if target.hardwareTarget.type["group"] == "extra":
				target.Activate()

	def _StartEndgame(self):
		ms = self._GetMothership()
		ms.Activate()
		for part in self._GetMothershipParts():
			part.Activate()
			part.SetOwner(self.alienFaction)
		ms.SetOwner(self.alienFaction)
		self._SetMothershipCountdown()
	
	def _SetMothershipCountdown(self):
		reloadTime=self.conf.mothershipBaseReload + self.conf.mothershipScalingReload * self.occupiedArea[self._GetMothership().owner]/self.totalArea
		print("reload time: {} - occupied area: {}, total area: {}".format(reloadTime, self.occupiedArea[self._GetMothership().owner], self.totalArea))
		CountdownTimer.Add(self._MothershipFire, reloadTime)
	
	## Check whether all mothership parts have the same alignment and set alignment for whole mothership accordingly
	def _CheckMothershipAlignment(self):
		parts = self._GetMothershipParts()
		owners = set([p.owner for p in parts])
		if len(owners) == 1 and parts[0].owner != self._GetMothership().owner: # all parts owned by the same owner
			self._GetMothership().SetOwner(parts[0].owner)

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
		self._CheckMothershipAlignment()

	def _GetMothershipParts(self):
		return [t for t in self.targets if t.hardwareTarget.type["group"] == "mothershipPart"]

	def _GetMothership(self):
		return [t for t in self.targets if t.hardwareTarget.type["group"] == "mothership"][0]


	def _MothershipFire(self):
		target = random.choice([t for t in self.targets if t.hardwareTarget.type["group"] == "simple"])
		if not target.protected:
			target.SetOwner(self._GetMothership().owner)
		self._SetMothershipCountdown()


