import Dummy
import domination
import shootingGallery
import Lobby

## \defgroup gamemodes Gamemodes
# Different rulesets for the game
## Exception that is thrown when the game is finished to break the game loop
availableModes = {
	"dummy":Dummy.GetClasses(),
	"domination":domination.GetClasses(),
	"shootingGallery":shootingGallery.GetClasses(),
	"lobby":Lobby.GetClasses()
	}
