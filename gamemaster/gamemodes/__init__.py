import Dummy
import Domination
import ShootingGallery
import Lobby

## \defgroup gamemodes Gamemodes
# Different rulesets for the game
## Exception that is thrown when the game is finished to break the game loop
availableModes = {
	"dummy":Dummy.GetClasses(),
	"domination":Domination.GetClasses(),
	"shootingGallery":ShootingGallery.GetClasses(),
	"lobby":Lobby.GetClasses()
	}
