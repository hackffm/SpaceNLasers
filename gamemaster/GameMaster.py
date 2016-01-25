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
gameEngine.Run()

