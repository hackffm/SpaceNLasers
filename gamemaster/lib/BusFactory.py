def setTargetColor(groupID, targetID, color):
	return "{grp}a{target}02{color}\n".format(grp=groupID,target=targetID,color=color)

def readyToShoot(weaponLetter):
	return "s{}\n".format(weaponLetter)

def shootNow():
	return "S\n"

def getWeaponButtons(weaponLetter):
	return "{}b\n".format(weaponLetter)

def readyToShoot(weaponLetter):
	return "s{}\n".format(weaponLetter)

def startShootingSequence():
	return "S\n"

def rumbleShootAnimation(weaponLetter):
	return "{}A011FF000401\n".format(weaponLetter)

def doSomethingAnimationLikeOnWeapon(weaponLetter): # TODO: please fix name here and in calling function
	return "{}a00704\n".format(weaponLetter)

def pollTargetState(targetGroupID):
	return "{}tr\n".format(targetGroupID)

def enableWeapon(weaponLetter):
	return "{}A102FF\n".format(weaponLetter)

class Constants:
	WEAPON_PRIMARY_BTN=1
