/*
 Light Sender for Arduino
 
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


#include "LightTx.h"

LightTxElementClass::LightTxElementClass(void) {
  Pin = 255;
  Visible = 0;
  Data = 0xff;  // 0 makes light on
  Enabled = 0;
}

LightTxElementClass::~LightTxElementClass(void) {
  Pin = 255;
}

void LightTxElementClass::setPin(uint8_t laserPin, uint8_t visiValue) {
  Pin = laserPin;
  Visible = visiValue;
  pinMode(Pin, OUTPUT);
  digitalWrite(Pin, LOW);
  analogWrite(Pin, Visible);
}

void LightTxElementClass::setVisible(uint8_t visiValue) {
  Visible = visiValue;
  analogWrite(Pin, Visible);
}

void LightTxElementClass::doTransmitBit(uint8_t state) {
  if(Pin != 255) {
    if(state == 0) {
      analogWrite(Pin, 0);
      digitalWrite(Pin, LOW);
    } else if((state >= 1) && (state <= 8)) {
      if(Enabled) {
        if(Data & (1<<(state - 1))) {
          // a 1 bit in data should make light on
          digitalWrite(Pin, HIGH);
        } else {
          digitalWrite(Pin, LOW);
        }
      }
    } else if(state == 9) {
      // Turn the visible light back on if needed
      analogWrite(Pin, Visible);
    }
  }
}

// *************************************

LightTxClass::LightTxClass(void) {
  shotTriggered = 0;
  state = 0;
  bitTime = 2000;
}

void LightTxClass::doTransmitBitAll(uint8_t state) {
  if((!shotTriggered) && (state >= 1) && (state <=8)) return;
  for(int8_t i = 0; i < MAXTXELM; i++) {
    TxElm[i].doTransmitBit(state);
  }
}

void LightTxClass::triggerShot(void) {
  shotTriggered = 1;
}

void LightTxClass::startTransmit(void) {
  state = 0;
  timestamp = (uint16_t)micros();
  doTransmitBitAll(state);  
  state++;
}

uint8_t LightTxClass::doTransmit(void) {
  if(!state) return(0);
  if(((uint16_t)micros() - timestamp) > bitTime) {
    timestamp += bitTime;
    doTransmitBitAll(state);
    state++;
    if(state >= 10) {
      state = 0;
      shotTriggered = 0;
      return(0);
    }
  }
  return(1);
}
