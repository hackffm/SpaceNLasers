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

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=64)
pygame.mixer.set_num_channels(20)

# load audio files in list
soundFiles = {
	"intro": "intro.wav",
	"gameOver": "gameover.wav",
	"gameOverJingle": "gameoverjingle.wav",
	"boing8bit": "boing8bit.wav",
	"music": "music.wav",
	"start": "start.wav",
	"laserblaster":"laser1.wav",
	"targetDestroyed":"explo_robot_down.wav"
}
sounds = {k:pygame.mixer.Sound("sounds/{soundtheme}/{filename}".format(soundtheme="default", filename=v)) for k, v in soundFiles.iteritems()}

# init serial comunication
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0', 38400)

# init game engine class and wait for menugod
gameEngine = GameEngine(gameHotLine, sounds, args.hwconfig, args.menugod, args.beamer)


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

try:
	gameEngine.Run()
except KeyboardInterrupt:
	gameHotLine.Close()

