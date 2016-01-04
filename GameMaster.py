#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import time
import pygame
import os

#########################################
# game class import 
from GameWorld import GameWorld
from lib.GameEngine import GameEngine
from lib.SerialHalfDuplex import SerialHalfDuplex
from lib.LaserWeapon import LaserWeapon
from lib.GameScreen import GameScreen


#########################################
# init game screen 
myScreen = GameScreen("")
#myScreen.initScreenDevice()
#myScreen.fillBackground((0,0,0))


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
gameHotLine = SerialHalfDuplex()
gameHotLine.configSerial('/dev/ttyUSB0',38400) # init serial


#########################################
# init game world class
gameWorld = GameWorld() # create game world
gameWorld.sounds = sounds


#########################################
# init laser class
laserWeapon = LaserWeapon() # create laser weapon
gameWorld.AddLaserWeapon(laserWeapon)

#########################################
# init targets

# targets begins with digital pin 4,5,6,7,8,11
# sensors anlog pins from 0-

# init target group 1
gameWorld.AddTargetGroup('1',0) # id, z-index
#newTargetGroup.AddTarget('0',0)
gameWorld.GetTargetGroupByID('1').AddTarget('1',1) # id, z-index
gameWorld.GetTargetGroupByID('1').AddTarget('2',2) # id, z-index
gameWorld.GetTargetGroupByID('1').AddTarget('3',3) # id, z-index

# init target group 2
gameWorld.AddTargetGroup('2',0)
gameWorld.GetTargetGroupByID('2').AddTarget('0',0)
gameWorld.GetTargetGroupByID('2').AddTarget('1',1)
gameWorld.GetTargetGroupByID('2').AddTarget('2',2)
# gameWorld.GetTargetGroupByID('2').AddTarget('3',3)

# init target group 3
gameWorld.AddTargetGroup('3',0)
# newTargetGroup.AddTarget('0',0)
gameWorld.GetTargetGroupByID('3').AddTarget('0',1)
gameWorld.GetTargetGroupByID('3').AddTarget('1',2)
gameWorld.GetTargetGroupByID('3').AddTarget('2',3)
gameWorld.GetTargetGroupByID('3').AddTarget('3',3)

# init target group 4
# target blitz and flash effect

newTargetGroup = gameWorld.AddTargetGroup('4',0)
gameWorld.GetTargetGroupByID('4').AddTarget('0',1)
gameWorld.GetTargetGroupByID('4').AddTarget('1',2)

gameWorld.GetTargetGroupByID('4').GetTargetByID('0').targetLEDAniHeader = '4a0'
gameWorld.GetTargetGroupByID('4').GetTargetByID('1').targetLEDAniHeader = '4a0'

gameWorld.GetTargetGroupByID('4').GetTargetByID('0').targetLEDSerialCode_Hit = '10FF000008'
gameWorld.GetTargetGroupByID('4').GetTargetByID('1').targetLEDSerialCode_Hit = '10FF000008'

gameWorld.GetTargetGroupByID('4').GetTargetByID('0').targetLEDSerialCode_HitReady = '1000FFFFAA'
gameWorld.GetTargetGroupByID('4').GetTargetByID('1').targetLEDSerialCode_HitReady = '1000FFFFAA'

gameWorld.GetTargetGroupByID('4').GetTargetByID('0').targetLEDSerialCode_Off = '1000000000'
gameWorld.GetTargetGroupByID('4').GetTargetByID('1').targetLEDSerialCode_Off = '1000000000'



# newTargetGroup.AddTarget('2',2)
# newTargetGroup.AddTarget('3',3)



#########################################
# init game engine class
gameEngine = GameEngine(gameHotLine, gameWorld, myScreen)


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

# gameHotLine.Ping('1a002000000\n')
# gameHotLine.Ping('1a10200FF00\n')
# gameHotLine.Ping('1a202FF00FF\n')
# gameHotLine.Ping('1a302FFFF00\n')


# gameHotLine.Ping('2a002FF0000\n')
# gameHotLine.Ping('2a10200FF00\n')
# gameHotLine.Ping('2a202FF00FF\n')
# gameHotLine.Ping('2a302FFFF00\n')


# gameHotLine.Ping('3a002FF0000\n')
# gameHotLine.Ping('3a10200FF00\n')
# gameHotLine.Ping('3a202FF00FF\n')
# gameHotLine.Ping('3a302FFFF00\n')

# gameHotLine.Ping('4a0100000FF08\n')


print 'debug target start';
print gameHotLine.PingPong('1t1\n') # debug target group
print gameHotLine.PingPong('1t2\n') # debug target group
print gameHotLine.PingPong('1t3\n') # debug target group
print gameHotLine.PingPong('1t4\n') # debug target group
print gameHotLine.PingPong('1t5\n') # debug target group
print gameHotLine.PingPong('1t6\n') # debug target group
print gameHotLine.PingPong('1t7\n') # debug target group
print gameHotLine.PingPong('1t8\n') # debug target group

print gameHotLine.PingPong('2t1\n') # debug target group
print gameHotLine.PingPong('3t1\n') # debug target group
print gameHotLine.PingPong('4t1\n') # debug target group
print 'debug target stop';

for tg in gameWorld.targetGroupList:
  for tar in tg.targetsList:
    print 'tg: '+tg.targetGroupID+' tar: '+tar.targetID   

# gameHotLine.Ping('4A120FF040408\n') # blitz kommando

gameHotLine.Ping('1A020FF040a08\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]

try:
 gameEngine.MainLoop()
 #bla = None
  
        
except KeyboardInterrupt:
  gameHotLine.Close()




"""
Hilfen:
  String parsen auf Hex-to-Dezimal: a="xx7Fyy", b=eval("0x"+a[2:4]) Achtung: 2:4 => 2 bis nicht einschließlich 4!
  String generieren mit genau 2 Hex-Digits: a=7, b="%0.2X"%a
  
  Zeitstempel: (Fließkommazahl wird zurückgegeben, Ganzzahlteil sind die Sekunden)
    import time 
    start_time = time.time() 
    ... 
    end_time = time.time() 
    delta_seconds = end_time - start_time 
    delta_milliseconds = delta_seconds * 1000

"""

