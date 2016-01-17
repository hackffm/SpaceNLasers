## \ingroup domination
class Config(object):
	def __init__(self):
		## Time after capturing during the target is immune to re-capturing
		self.targetProtectionDuration = 0.5

		## Scaling factor for scores
		self.scoreFactor = 1000.0

		## Time after which "extra" targets are activated
		self.buildupDuration = 10.0

		## Time after which the mothership is activated
		self.endgameTime = 5.0

		## Activate a new target every newTargetTime seconds
		self.newTargetTime = 1.0

		## Number of targets active at gamestart
		self.startupTargetCount = 1

		## Reload time for the mothership weapon
		self.mothershipReload = 2.0

		## Initial color of the alien mothership
		self.alienFactionColor = "8400FF"


