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

		## Base reload time for the mothership weapon
		# \see mothershipScalingReload
		self.mothershipBaseReload = 0.5

		## Scaling reload time for the mothership weapon
		# Reload time that is dependent on the percentage of domination area (roughly equivalent to percentage of targets) owned by the faction occupying the mothership.
		# Total reload time is calculated as mothershipBaseReload + mothershipScalingReload * percentageOwnedByMothershipFaction
		# Set mothershipBaseReload to the minimum reloading time (which is essentially in place when the mothership just arrived).
		# Set mothershipScalingReload to the maximum reloading time when all targets are occupied by the mothership faction minus mothershipBaseReload.
		self.mothershipScalingReload = 2.0

		## Initial color of the alien mothership
		self.alienFactionColor = "8400FF"


