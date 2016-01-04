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
# init serial comunication
gameHotLine = SerialHalfDuplex()
gameHotLine.configSerial('/dev/ttyUSB0',38400) # init serial


#########################################
# init game world class
gameWorld = GameWorld() # create game world


gameHotLine.Ping('AA10200\n')
time.sleep(0.1)
gameHotLine.Ping('BA10200\n')
time.sleep(0.1)


gameHotLine.Ping('1T00FF\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('2T0050\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('3T0020\n') # set treshold to 205
time.sleep(0.1)
gameHotLine.Ping('4T0020\n') # set treshold to 205
time.sleep(0.1)

gameHotLine.Ping('1a002FF00FF\n')
gameHotLine.Ping('1a10200FF00\n')
gameHotLine.Ping('1a202FF00FF\n')
gameHotLine.Ping('1a302FFFF00\n')


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
print gameHotLine.PingPong('2t1\n') # debug target group
print gameHotLine.PingPong('3t1\n') # debug target group
print gameHotLine.PingPong('4t1\n') # debug target group
print 'debug target stop';

for tg in gameWorld.targetGroupList:
  for tar in tg.targetsList:
    print 'tg: '+tg.targetGroupID+' tar: '+tar.targetID  


#for x in ["1","2","3","4"]:
#  gameHotLine.Ping(x+'a002ff0000\n')
#  gameHotLine.Ping(x+'a102ffff00\n')
#  gameHotLine.Ping(x+'a202ff00ff\n')
#  gameHotLine.Ping(x+'a30200ff00\n')
#  gameHotLine.Ping(x+'a40200ffff\n') 

# gameHotLine.Ping('4A120FF040408\n') # blitz kommando

# gameHotLine.Ping('1A020FF040a08\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]




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

