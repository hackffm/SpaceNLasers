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
gameHotLine = SerialHalfDuplex('/dev/ttyUSB0',38400) # init serial
gameHotLine.Ping('\n\n')

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

for x in sys.argv[1:]:
  print x
  print gameHotLine.PingPong(x+'\n')

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

