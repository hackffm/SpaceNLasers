import json
from dialog import Dialog
from lib.SerialHalfDuplex import SerialHalfDuplex

hwconfigName="testbox"
serialPort="/dev/ttyUSB0"

d = Dialog(dialog="dialog")
d.set_background_title("Testing configuration {} on {}".format(hwconfigName, serialPort))
targetList = []
selectedTargets = [] # list of indices
gameHotLine = SerialHalfDuplex(serialPort, 38400)


with open("hardwareconfig/{}.json".format(hwconfigName), "r") as fp: # TODO: cmdline parameter
	hwconfig = json.load(fp)
with open("hardwareconfig/global.json", "r") as fp:
	config = json.load(fp)

class AbortException(BaseException):
	pass

def Menu(title, options, raiseOnAbort=True):
	code, tag = d.menu(title, choices=[(str(i), option[0]) for i, option in enumerate(options)])
	if code == d.OK:
		options[int(tag)][1]()
	else:
		if raiseOnAbort:
			raise AbortException("abort")

def MainMenu():
	Menu("Main menu", options=[
		("Global codes", GlobalCode),
		("Target codes", TargetCode),
		("Manual ping", Ping),
		("Manual pingpong", PingPong)])

def Ping():
	code = raw_input("command:")
	ExecuteCode(code)

def PingPong():
	code = raw_input("command:")
	result=ExecuteCode(code, waitForReturn=True)
	d.msgbox(result)

def ExecuteCode(code, waitForReturn=False):
	print(code)
	#return code
	if waitForReturn:
		return gameHotLine.PingPong(code)
	else:
		gameHotLine.Ping(code)

def GlobalCode():
	effects = hwconfig["globalEffects"]
	Menu("Global effect", options=[(name, lambda: ExecuteCode(code)) for name, code in effects.iteritems()])

def TargetCode():
	while(True):
		try:
			effects = config["targetTypes"]["simple"]["effects"]
			Menu("Target effect", options=[("Choose targets (currently {} selected)".format(len(selectedTargets)), ChooseTargets)]+[(name, lambda: ExecuteTargetCode(code)) for name, code in effects.iteritems()])
		except AbortException:
			break


def InitTargetList():
	global selectedTargets
	for groupID, group in hwconfig["targetControllers"].iteritems():
		for target in group["targets"]:
			text = "{}.{} ({})".format(groupID, target["id"], target["type"])
			targetList.append((target, text, groupID))
	selectedTargets=[i for i in range(len(targetList))]

def ChooseTargets():
	global selectedTargets
	choices = [(str(i), target[1], i in selectedTargets) for i, target in enumerate(targetList)]
	print(choices)
	code, tags = d.checklist("Select targets", choices=choices)
	if code == d.OK:
		selectedTargets = [int(tag) for tag in tags]

def ExecuteTargetCode(code):
	for index in selectedTargets:
		target = targetList[index][0]
		groupID = targetList[index][2]
		ExecuteCode(code.format(targetGroup=groupID, targetID=target["id"]))

InitTargetList()
while(True):
	try:
		MainMenu()
	except AbortException:
		break
