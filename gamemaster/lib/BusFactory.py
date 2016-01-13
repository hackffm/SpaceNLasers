def SetTargetColor(groupID, targetID, color):
	return "{grp}a{target}02{color}\n".format(grp=groupID, target=targetID, color=color)

def ReadyToShoot(weaponLetter):
	return "s{}\n".format(weaponLetter)

def ShootNow():
	return "S\n"

def GetWeaponButtons(weaponLetter):
	return "{}b\n".format(weaponLetter)

def StartShootingSequence():
	return "S\n"

def RumbleShootAnimation(weaponLetter):
	return "{}A011FF000401\n".format(weaponLetter)

def DoSomethingAnimationLikeOnWeapon(weaponLetter): # TODO: please fix name here and in calling function
	return "{}a00704\n".format(weaponLetter)

def PollTargetState(targetGroupID):
	return "{}tr\n".format(targetGroupID)

def EnableWeapon(weaponLetter):
	return "{}A102FF\n".format(weaponLetter)

class Constants(object):
	WEAPON_PRIMARY_BTN = 1
