
class GameOverException(BaseException):
	##
	# \param scores <Player>:int dictionary
	def __init__(self, scores):
		self.scores = scores

class Gamemode(object):
	def __init__(self, duration, gameEngine, players):
		self.duration = duration
		self.durationLeft = duration
		self.gameEngine = gameEngine
		self.scores = {p:0.0 for p in players}

	def Init(self):
		pass

	def Update(self, dt):
		if self.durationLeft is not None:
			self.durationLeft -= dt
			if self.durationLeft <= 0:
				raise GameOverException(self.scores)

	def SetTargets(self, targets):
		self.targets = targets


