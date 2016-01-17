## \defgroup domination domination
# \ingroup gamemodes
# Capture and hold targets to get points
# \{
#
# Targets that are hit by a player change to his color.
# Targets are immune against re-capturing for a short time.
# The more targets have the player color, the faster this player's score increases.
# Targets are introduced step-by step.
#
# \page mothership The alien mothership
# During the game, the alien mothership arrives.
# The mothership also captures targets and sets them to its own color.
# If the mothership is captured by a player, it will capture targets for him.
# \}

import target
import gamemode

def GetClasses():
	return {"targetClass":target.Target, "masterClass":gamemode.Gamemode}
