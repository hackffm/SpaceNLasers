/*
 Light Receiver for Arduino
 
 More information in header file at our website:
 http://www.hackerspace-ffm.de/wiki/index.php?title=SpaceInLasers
 
 Copyright (c) 2015, Lutz Lisseck (lutz. lisseck gmx. de)
 
 MIT-License: 
 Permission is hereby granted, free of charge, to any person obtaining a 
 copy of this software and associated documentation files (the 
 "Software"), to deal in the Software without restriction, including 
 without limitation the rights to use, copy, modify, merge, publish, 
 distribute, sublicense, and/or sell copies of the Software, and to 
 permit persons to whom the Software is furnished to do so, subject to 
 the following conditions: The above copyright notice and this permission 
 notice shall be included in all copies or substantial portions of the 
 Software. 
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY 
 KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE. 

*/

#include <Arduino.h>


#include "LightRx.h"

LightRxElementClass::LightRxElementClass(void) {
  Pin = 255;
  Threshold = 250;
  Pullup = 1;
  Data = 0;
}

LightRxElementClass::~LightRxElementClass(void) {
  Pin = 255;
}

void LightRxElementClass::setPin(uint8_t analogPin, uint8_t pullupOn) {
  Pin = analogPin;
  Pullup = pullupOn ? 1:0;
  pinMode(Pin, Pullup ? INPUT_PULLUP : INPUT);
}

void LightRxElementClass::doReceiveBit(uint8_t state) {
  if(Pin != 255) {
    if(state == 0) {
        digitalWrite(10, HIGH);
      DarkValue = analogRead(Pin);
      Data = 0;
      MaxValue = DarkValue;
      MinValue = DarkValue;
        digitalWrite(10, LOW);
    } else if((state >= 1) && (state <= 8)) {
        digitalWrite(10, HIGH);
      uint16_t v = analogRead(Pin);
      if(v > MaxValue) MaxValue = v;
      if(v < MinValue) MinValue = v;
      // If target got light, value will be low and bit will get set
      if(((int16_t)DarkValue - (int16_t)v) > (int16_t)Threshold) {
        Data |= (1<<(state - 1));
      } 
        digitalWrite(10, LOW);
    }
  }
}

// *************************************

LightRxClass::LightRxClass(void) {
  state = 0;
  bitTime = 2000;
  bitDelay = 300;
}

void LightRxClass::doReceiveBitAll(uint8_t state) {
  for(int8_t i = 0; i < MAXRXELM; i++) {
    RxElm[i].doReceiveBit(state);
  }
}

void LightRxClass::startReceive(void) {
  state = 0;
  delayMicroseconds(bitDelay);
  timestamp = (uint16_t)micros();
  doReceiveBitAll(state);  
  state++; 
}

uint8_t LightRxClass::doReceive(void) {
  if(!state) return(0);
  if(((uint16_t)micros() - timestamp) > bitTime) {
    timestamp += bitTime;
    doReceiveBitAll(state);
    state++;
    if(state >= 10) {
      state = 0;
      return(0);
    }
  }
  return(1);
}
