#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import time
import pygame
import os
import argparse

from lib.GameEngine import GameEngine
from lib.SerialHalfDuplex import SerialHalfDuplex
from lib.Weapon import Weapon

# parse arguments
parser=argparse.ArgumentParser(description="SpaceNLasers game master")
parser.add_argument("hwconfig", type=str, help="a json file describing the current hardware setup")
parser.add_argument("--menugod",type=str, nargs="?", default=None, const="", help="IP of menugod to connect to. Leave empty to run in server mode. Omit this option to use a FakeMenuGod for testing")
args=parser.parse_args()

# init audio mixer
os.system("amixer cset numid=3 1")
os.system("amixer set PCM -- 1000")

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=64)
pygame.mixer.set_num_channels(20)

# load audio files in list
sounds = {
"mixer": pygame.mixer,
"introSound": pygame.mixer.Sound("sounds/intro.wav"), 
"gameOverSound": pygame.mixer.Sound("sounds/gameover.wav"), 
"gameOverJingleSound": pygame.mixer.Sound("sounds/gameoverjingle.wav"), 
"boing8bitSound": pygame.mixer.Sound("sounds/boing8bit.wav"), 
"musicSound": pygame.mixer.Sound("sounds/music.wav"), 
"startSound": pygame.mixer.Sound("sounds/start.wav"), 
"laserblasterSound":pygame.mixer.Sound("sounds/laser1.wav"), 
"explosionSound":pygame.mixer.Sound("sounds/explo_robot_down.wav")
}

# init serial comunication
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0',38400)

# init game engine class and wait for menugod
gameEngine = GameEngine(gameHotLine, sounds, args.hwconfig, args.menugod)


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

