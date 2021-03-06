#!/usr/bin/python
# -*- coding: utf-8 -*-

import Tkinter as tk

import time
import pygame
import os
import sys

#########################################
# game class import 

from lib.SerialHalfDuplex import SerialHalfDuplex

#########################################
# init serial comunication
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0',38400)
gameHotLine.Ping('\n\n')

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

#while (1):
for x in ["1","2","3","4"]:
  gameHotLine.Ping(x+'a002ff0000\n')
  gameHotLine.Ping(x+'a102ffff00\n')
  gameHotLine.Ping(x+'a202ff00ff\n')
  gameHotLine.Ping(x+'a30200ff00\n')
  gameHotLine.Ping(x+'a40200ffff\n')

gameHotLine.Ping('1A002ff\n')
gameHotLine.Ping('1A102ff\n')
gameHotLine.Ping('s\n')
time.sleep(0.4)  
gameHotLine.Ping('4a01000808000 \n')
time.sleep(0.4)
gameHotLine.Ping('S\n')

      
#  for x in ["1","2","3","4"]:
#    for y in ["0","1","2","3","4"]:
#      gameHotLine.Ping(x+'a'+y+'02000000\n')
#      if x=='4' and y=='0':
#        time.sleep(0.4)
  
#gameHotLine.PinPong()
gameHotLine.Close()
#gameHotLine.Ping('AA10200\n')
#gameHotLine.Ping('BA10200\n')

# gameHotLine.Ping('4A120FF040408\n') # blitz kommando

#gameHotLine.Ping('1A020FF040a08\n') # [id][animation trigger][laserid 0 / 1][ani id 20][FF040a][flash count 08 for 8 time flash]
  




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

