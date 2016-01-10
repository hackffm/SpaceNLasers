import BusFactory
class Weapon:
	def __init__(self,code,shotCode):
		self.code=code
		self.shotCode=shotCode
		self.player=None
		self.cooloff=0.0
		self.heat=0.0
	
	## parse state from bus
	def SetCurrentState(self,stateCode):
		buttonState=int(eval("0x"+stateCode[0:2]))
		self.primaryPressed = bool(buttonState & BusFactory.Constants.WEAPON_PRIMARY_BTN)
	
	## virtual weapon logic (cooloff etc.)
	def Update(self,dt):
		self.heat-=dt

	## Return whether shot is fired this round
	def ShootsThisFrame(self):
		if self.heat<0.0 and self.primaryPressed:
			self.heat=self.cooloff
			return True
		return False
