## \defgroup shootingGallery shootingGallery
# \ingroup gamemodes
# A simple "free for all" shoot 'em up
# \{
#
# Targets are activated randomly.
# Hitting an activated target gives a certain amount of points and disables the target again.
# Hits are visualised by changing the target to the player color for a short time.
#
# \}

import target
import gamemode

def GetClasses():
	return {"targetClass":target.Target, "masterClass":gamemode.Gamemode}
