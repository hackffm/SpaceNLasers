/*
 FastLED animations for Arduino
 
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

#include "AnalogAnim.h"


AnalogElementClass::AnalogElementClass(void) {
	Flags = 0;
	EffectNumber = 0;
	State = 0;
	OutputID = 0;
	pAnalogSet = NULL;
}

AnalogElementClass::~AnalogElementClass(void) {

}

void AnalogElementClass::directSet(uint8_t value) {
	LastValue = value;
	if(!pAnalogSet) {
		// Arduino pin if not OutputID not 0
		if(OutputID) analogWrite(OutputID, value);
	} else {
		pAnalogSet(OutputID, value);
	}
}

void AnalogElementClass::mute(uint8_t onoff) {
	if(onoff) {
		Flags |= ANIFLAGBLANK;
		// Blank all
		if(!pAnalogSet) {
			// Arduino pin if not OutputID not 0
			if(OutputID) analogWrite(OutputID, 0);
		} else {
			pAnalogSet(OutputID, 0);
		} 
	} else {
		Flags &= ~ANIFLAGBLANK;
		directSet(LastValue);
	}
}

void AnalogElementClass::startAnimation(uint8_t EffectNo) {
	if(!pAnalogSet && !OutputID) return;
	EffectNumber = EffectNo;
	
	if(Flags & ANIFLAGBLANK) return;
	
	switch(EffectNumber) {
		case 0:
			// Do nothing.
			break;
			
		case 1:
			// Blank all
			directSet(0);      
			break;
			
		case 2:
			// Set all to argument 
			directSet(Arguments[0]);      
			break;      
			
			
		case 8:
			//Palette action
 
			break;    
		
		// Fade Up: StartVal 0, StopVal 1, Speed [0.1 ms delay] 2, Repeat 3 
		case 0x10: // Up
		case 0x11: // Down
			Timestamp = micros();
			directSet(Arguments[0]);
			Storage8[0] = Arguments[3];
			Storage32 = Arguments[2] * 100;
			break;
			
		// Flash: OnVal 0, OnTime [10ms] 1, OffTime [10ms] 2, Repeat 3
		case 0x20:
			Timestamp = millis();   
			Storage8[0] = Arguments[3];      
			Storage32 = Arguments[1] * 10;
			directSet(Arguments[0]);
			Storage8[1] = 1;
			break;   

		// ufo motor control
		// Arguments[0]: 0-255
		// Arguments[1]: 0-255
		case 0x30:
			analogWrite(9,Arguments[0]); // );
			analogWrite(10,Arguments[1]); // );
			break;

	
	}  
}

void AnalogElementClass::worker(void) {
	if(!pAnalogSet && !OutputID) return;
	if(Flags & ANIFLAGBLANK) return;
	
	switch(EffectNumber) {
		case 0:
		case 1:
		case 2:
			// Do nothing.
			break;
			
		case 8:
			//Palette action

			break;    
		
		case 0x10: // up
			if((micros() - Timestamp) > Storage32) {
				Timestamp += Storage32;
				if(LastValue >= Arguments[1]) {
					LastValue = Arguments[0];
					Serial.print(Arguments[3]);
					if(Arguments[3]) {
						Storage8[0]--;
						if(Storage8[0] == 0) EffectNumber = 0;
					}
				} else {
					LastValue++;
				}
				directSet(LastValue);
			}
			break;
			
		case 0x11: // down
			if((micros() - Timestamp) > Storage32) {
				Timestamp += Storage32;
				if(LastValue <= Arguments[1]) {
					LastValue = Arguments[0];
					if(Arguments[3]) {
						Storage8[0]--;
						if(Storage8[0] == 0) { EffectNumber = 0; LastValue = Arguments[1];}
					}
				} else {
					LastValue--;
				}
				directSet(LastValue);
			}
			break;  
			
		case 0x20: // Flash
			if(((uint16_t)millis() - (uint16_t)Timestamp) > (uint16_t)Storage32) {
				Timestamp += (uint16_t)Storage32;
				if(Storage8[1]) {
					Storage8[1] = 0;
					directSet(0); 
					Storage32 = Arguments[2] * 10;
					if(Arguments[3]) {
						Storage8[0]--;
						if(Storage8[0] == 0) EffectNumber = 0;
					}          
				} else {
					Storage8[1] = 1;
					directSet(Arguments[0]);
					Storage32 = Arguments[1] * 10;
				}
			}
			break;    
	}

}

// ********** MULTICLASS STUFF ****************

AnalogClass::AnalogClass(void) {

}

void AnalogClass::worker(void) {
	for(int8_t i = 0; i < MAXANALOGELM; i++) {
		AnimElm[i].worker();
	}
}

void AnalogClass::shotMute(uint8_t onoff) {
	for(int8_t i = 0; i < MAXANALOGELM; i++) {
		if(AnimElm[i].Flags & ANIFLAGSHOTBLANK) {
			AnimElm[i].mute(onoff);
		}
	}
}
