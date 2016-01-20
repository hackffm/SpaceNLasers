#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import argparse
import pygame

from lib.GameEngine import GameEngine
from lib.SerialHalfDuplex import SerialHalfDuplex

# parse arguments
parser = argparse.ArgumentParser(description="SpaceNLasers game master")
parser.add_argument("hwconfig", type=str, help="a json file describing the current hardware setup")
parser.add_argument("--menugod", type=str, nargs="?", default=None, const="", help="IP of menugod to connect to. Leave empty to run in server mode. Omit this option to use a FakeMenuGod for testing")
parser.add_argument("--beamer", type=str, nargs="?", default=None, const="", help="IP of beamer to connect to. Leave empty to run in server mode. Omit this option to disable beamer output")
args = parser.parse_args()

# init audio mixer
if False:
	os.system("amixer cset numid=3 1")
	os.system("amixer set PCM -- 1000")

# init serial comunication
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0', 38400)

# init game engine class and wait for menugod
gameEngine = GameEngine(gameHotLine, args.hwconfig, args.menugod, args.beamer)


gameHotLine.Ping('AA10200\n')
time.sleep(0.1)
gameHotLine.Ping('BA10200\n')

gameHotLine.Ping('1T00FF\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('2T0050\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('3T0020\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('4T0020\n') # set treshold to 205
time.sleep(0.1)

gameEngine.Run()

