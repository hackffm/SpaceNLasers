#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import time
import pygame
import os

#########################################
# game class import 
from lib.GameEngine import GameEngine
from lib.SerialHalfDuplex import SerialHalfDuplex
from lib.Weapon import Weapon



#########################################
# init audio mixer
os.system("amixer cset numid=3 1")
os.system("amixer set PCM -- 1000")

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=64)
pygame.mixer.set_num_channels(20)

#########################################
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

#########################################
# init serial comunication
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0',38400)


#########################################


#########################################
# init laser class
#weaponA=Weapon("A",145)
#gameWorld.AddLaserWeapon(weaponA)

#########################################
# init targets

# targets begins with digital pin 4,5,6,7,8,11
# sensors anlog pins from 0-

# init target group 1


#########################################
# init game engine class
gameEngine = GameEngine(gameHotLine, sounds)


gameHotLine.Ping('AA10200\n')
time.sleep(0.1)
gameHotLine.Ping('BA10200\n')

# gameHotLine.Ping('t250\n') # set treshold to 205

# gameHotLine.Ping('t030\n') # set treshold to 205

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

"""
Hilfen:
  String parsen auf Hex-to-Dezimal: a="xx7Fyy", b=eval("0x"+a[2:4]) Achtung: 2:4 => 2 bis nicht einschließlich 4!
  
  Zeitstempel: (Fließkommazahl wird zurückgegeben, Ganzzahlteil sind die Sekunden)
    import time 
    start_time = time.time() 
    ... 
    end_time = time.time() 
    delta_seconds = end_time - start_time 
    delta_milliseconds = delta_seconds * 1000

"""

