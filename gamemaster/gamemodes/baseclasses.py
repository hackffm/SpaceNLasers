
class GameOverException(BaseException):
	pass

class Gamemode(object):
	def __init__(self, duration, gameEngine):
		self.duration = duration
		self.durationLeft = duration
		self.gameEngine = gameEngine

	def Init(self):
		pass

	def Update(self, dt):
		if self.durationLeft is not None:
			self.durationLeft -= dt
			if self.durationLeft <= 0:
				raise GameOverException()

	def SetTargets(self, targets):
		self.targets = targets


