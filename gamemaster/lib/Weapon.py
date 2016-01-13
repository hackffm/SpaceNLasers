import BusFactory
class Weapon(object):
	def __init__(self, code, shotCode):
		self.code = code
		self.shotCode = shotCode
		self.player = None
		self.cooloff = 0.0
		self.heat = 0.0
		self.primaryWasReleased = True

	## parse state from bus
	def SetCurrentState(self, stateCode):
		buttonState = int(stateCode[0:2], 16)
		self.primaryPressed = bool(buttonState & BusFactory.Constants.WEAPON_PRIMARY_BTN)
		if not self.primaryPressed:
			self.primaryWasReleased = True

	## virtual weapon logic (cooloff etc.)
	def Update(self, dt):
		self.heat -= dt

	## Return whether shot is fired this round
	def ShootsThisFrame(self):
		if self.heat < 0.0 and self.primaryPressed and self.primaryWasReleased:
			self.heat = self.cooloff
			self.primaryWasReleased = False
			return True
		return False
