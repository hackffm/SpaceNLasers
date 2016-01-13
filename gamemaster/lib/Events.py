class Event:
	def __init__(self, time):
		self.time = time

class TargetHitEvent(Event):
	"""Event when a hit on a target is detected"""
	def __init__(self, time, weapon, target):
		Event.__init__(self, time)
		self.weapon = weapon
		self.target = target
