## \ingroup shootingGallery
class Config(object):
	def __init__(self):
		## Time to show target in player color after hit
		self.owningTime = 2.0

		## Time after which an active target is disabled if not hit
		self.activeTimeout = 5.0

		## Maximum number of concurrently active targets
		self.maximumActiveTargets = 1

		## Increase to produce new targets after hits more quickly
		self.newTargetProbabilityModifier = 1.0

