import random
import lib.Target
from lib.CountdownTimer import CountdownTimer

class Target(lib.Target.Target):
	def __init__(self, hwTarget, gameModeMaster):
		lib.Target.Target.__init__(self, hwTarget)
		self.protectionTimer = CountdownTimer(lambda: None, 0.0)
		self.fadeoutTimer = CountdownTimer(lambda: None, 0.0)
		self.protected = False
		self.owner = None
		self.gameModeMaster = gameModeMaster
		self.active = False
		self.Effect("disable")

	def Activate(self):
		self.Effect("enable")
		self.active = True
		self.gameModeMaster.totalArea += self.hardwareTarget.scoreValue
	
	def Deactivate(self):
		self.Effect("disable")
		self.active = False
		self.SetColor("000000")
		self.gameModeMaster.totalArea -= self.hardwareTarget.scoreValue

	def Hit(self, event):
		if self.active and self.hardwareTarget.type["group"] != "mothership":
			lib.Target.Target.Hit(self, event)
			if not self.protected:
				self.SetOwner(event.weapon.player)

	def Update(self, dt):
		self.protectionTimer.Update(dt)
		self.fadeoutTimer.Update(dt)

	def _Unprotect(self):
		self.protected = False
		self.SetColor(self.owner.color)

	def SetOwner(self, player, nodestroy=False):
		if self.owner != player:
			if self.owner is not None:
				self.gameModeMaster.occupiedArea[self.owner] -= self.hardwareTarget.scoreValue
			if player is not None:
				self.Activate()
				self.gameModeMaster.occupiedArea[player] += self.hardwareTarget.scoreValue

				if not nodestroy:
					self.gameModeMaster.gameEngine.sound.targetDestroyed.play()
					self.Effect("destroy")
				
				if self.hardwareTarget.type["group"] == "simple":
					fadeout = self.gameModeMaster.conf.alienTargetTimeout if player is self.gameModeMaster.alienFaction else random.uniform(*self.gameModeMaster.conf.playerTargetTimeoutInterval)
					print("fadeout for player {} is {}".format(fadeout, player))
					self.fadeoutTimer = CountdownTimer(lambda: self.SetOwner(None), fadeout)

				self.SetColor(player.color)
				self.protectionTimer = CountdownTimer(self._Unprotect, self.gameModeMaster.conf.targetProtectionDuration)
				self.protected = True
			else:
				self.Deactivate()
			self.owner = player


