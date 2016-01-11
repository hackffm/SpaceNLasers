
class GameOverException:
	pass

class Gamemode:
	def __init__(self,duration,gameEngine):
		self.duration=duration
		self.durationLeft=duration
		self.gameEngine=gameEngine
	
	def Update(self,dt):
		if self.durationLeft is not None:
			self.durationLeft-=dt
			if self.durationLeft<=0:
				raise GameOverException()
	
	def SetTargets(self,targets):
		self.targets=targets

import Dummy
import Domination
import Lobby

available_modes={
	"dummy":Dummy.GetClasses(),
	"domination":Domination.GetClasses(),
	"lobby":Lobby.GetClasses()
	}
