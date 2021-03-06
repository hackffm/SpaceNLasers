#!/usr/bin/python3
import json
import sys
from dialog import Dialog
from lib.SerialHalfDuplex import SerialHalfDuplex

if len(sys.argv) != 2:
	sys.exit("USAGE: {} hardwareconfig".format(sys.argv[0]))
hwconfigName=sys.argv[1]
serialPort="/dev/ttyUSB0"

d = Dialog(dialog="dialog")
d.set_background_title("Testing configuration {} on {}".format(hwconfigName, serialPort))
targetList = []
selectedTargets = [] # list of indices
gameHotLine = SerialHalfDuplex(serialPort, 38400)


with open(hwconfigName, "r") as fp:
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
	code = input("command:")
	ExecuteCode(code+"\n")

def PingPong():
	code = input("command:")
	result=ExecuteCode(code+"\n", waitForReturn=True)
	print(result)
	input()

def ExecuteCode(code, waitForReturn=False):
	print(code)
	code = str(code)
	if len(code) > 0 and code[-1] != "\n":
		code += "\n"
	#return code
	input_tuples = tuple()
	while(True):
		try:
			formatted = code.format(*input_tuples)
			break
		except IndexError:
			input_tuples += (input("parameter:"),)
	
	if waitForReturn:
		return gameHotLine.PingPong(formatted.encode("utf-8"))
	else:
		gameHotLine.Ping(formatted.encode("utf-8"))

def GlobalCode():
	while(True):
		try:
			effects = hwconfig["globalEffects"]
			Menu("Global effect", options=[(name, lambda code=code: ExecuteCode(code)) for name, code in effects.items()]) # note the code=code to fix capturing
		except AbortException:
			break

def TargetCode():
	while(True):
		try:
			effects = config["targetTypes"]["simple"]["effects"]
			Menu("Target effect", options=
					[("Choose targets (currently {} selected)".format(len(selectedTargets)), ChooseTargets)]+
					[(name, lambda name=name: ExecuteTargetCode(name)) for name in effects]) # note the name=name to fix capturing
		except AbortException:
			break


def InitTargetList():
	global selectedTargets
	for groupID, group in hwconfig["targetControllers"].items():
		for target in group["targets"]:
			text = "{}.{} ({})".format(groupID, target["id"], target["type"])
			targetList.append((target, text, groupID))
	selectedTargets=[i for i in range(len(targetList))]

def ChooseTargets():
	global selectedTargets
	choices = [(str(i), target[1], i in selectedTargets) for i, target in enumerate(targetList)]
	code, tags = d.checklist("Select targets", choices=choices)
	if code == d.OK:
		selectedTargets = [int(tag) for tag in tags]

def ExecuteTargetCode(effectName):
	for index in selectedTargets:
		target = targetList[index][0]
		commandPattern = config["targetTypes"][target["type"]]["effects"][effectName]
		groupID = targetList[index][2]
		ExecuteCode(commandPattern.format(targetGroup=groupID, targetID=target["id"]))

InitTargetList()
while(True):
	try:
		MainMenu()
	except AbortException:
		break
