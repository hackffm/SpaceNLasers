import Dummy
import Domination
import ShootingGallery
import Lobby


class GameOverException(BaseException):
	pass

class Gamemode:
	def __init__(self, duration, gameEngine):
		self.duration = duration
		self.durationLeft = duration
		self.gameEngine = gameEngine

	def Init(self):
		pass

	def Update(self,dt):
		if self.durationLeft is not None:
			self.durationLeft -= dt
			if self.durationLeft <= 0:
				raise GameOverException()

	def SetTargets(self, targets):
		self.targets = targets

availableModes = {
	"dummy":Dummy.GetClasses(),
	"domination":Domination.GetClasses(),
	"shootingGallery":ShootingGallery.GetClasses(),
	"lobby":Lobby.GetClasses()
	}
