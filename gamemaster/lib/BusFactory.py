class InvalidBusReply(BaseException):
	def __init__(self, source, e, text):
		BaseException.__init__(self, text)
		self.source = source
		self.e=e

def ReadyToShoot(weaponLetter):
	return "s{}\n".format(weaponLetter)

def ShootNow():
	return "S\n"

def GetWeaponButtons(weaponLetter):
	return "{}b\n".format(weaponLetter)

def StartShootingSequence():
	return "S\n"

def RumbleShootAnimation(weaponLetter):
	return "{}A011A0000001\n".format(weaponLetter) # object=0, animation number=11, 

def DoSomethingAnimationLikeOnWeapon(weaponLetter): # TODO: please fix name here and in calling function
	return "{}a00704\n".format(weaponLetter)

def PollTargetState(targetGroupID):
	return "{}tr\n".format(targetGroupID)

def EnableWeapon(weaponLetter):
	return "{}A10240\n".format(weaponLetter)

class Constants(object):
	WEAPON_PRIMARY_BTN = 1
