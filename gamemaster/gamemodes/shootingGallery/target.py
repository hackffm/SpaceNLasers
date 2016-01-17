import lib.Target
from lib.CountdownTimer import CountdownTimer

class Target(lib.Target.Target):
	def __init__(self, hwTarget, gameModeMaster):
		lib.Target.Target.__init__(self, hwTarget)
		self.gameModeMaster = gameModeMaster

		self.timeout = CountdownTimer(lambda: None, 0.0)

		self.Deactivate()

	def Activate(self):
		print("target activated")
		self.active = True
		self.Effect("enable")
		self.timeout = CountdownTimer(self.Deactivate, self.gameModeMaster.conf.activeTimeout)

	def Deactivate(self):
		print("target deactivated")
		self.active = False
		self.owner = None
		self.Effect("disable")

	def Hit(self, event):
		lib.Target.Target.Hit(self, event)
		if self.active:
			print("hit!")
			self.gameModeMaster.gameEngine.PlaySoundAndWait("targetDestroyed", 0)
			self.active = False
			self.owner = event.weapon.player
			self.SetColor(event.weapon.player.color)
			self.timeout = CountdownTimer(self.Deactivate, self.gameModeMaster.conf.owningTime)
			self.gameModeMaster.AddPoint(event.weapon.player, self.hardwareTarget.scoreValue)

	def Update(self, dt):
		self.timeout.Update(dt)

