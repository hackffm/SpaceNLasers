
class GameOverException:
	pass

class Gamemode:
	def __init__(self,duration):
		self.durationLeft=duration
	
	def Update(self,dt):
		if self.durationLeft is not None:
			self.durationLeft-=dt
			if self.durationLeft<=0:
				raise GameOverException()

import Dummy
import Domination
import Lobby

available_modes={
	"dummy":Dummy.GetClasses(),
	"domination":Domination.GetClasses(),
	"lobby":Lobby.GetClasses()
	}
