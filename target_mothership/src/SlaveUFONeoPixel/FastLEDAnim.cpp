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

#include "FastLED.h"

#include "FastLEDAnim.h"


AnimElementClass::AnimElementClass(void) {
  Flags = 0;
  LedCount = 0;
  EffectNumber = 0;
  State = 0;
  pLeds = NULL;
}

AnimElementClass::~AnimElementClass(void) {

}

void AnimElementClass::mute(uint8_t onoff) {
  if(onoff) {
    Flags |= ANIFLAGBLANK;
    // Blank all
    for(uint8_t i = 0; i < LedCount; i++) {
      pLeds[i] = CRGB::Black;
    } 
  } else {
    Flags &= ~ANIFLAGBLANK;
  }
}

void AnimElementClass::startAnimation(uint8_t EffectNo) {
  if(!pLeds || !LedCount) return;
  EffectNumber = EffectNo;
  uint8_t brightness;

  if(Flags & ANIFLAGBLANK) return;
  
  switch(EffectNumber) {
    case 0:
      // Do nothing.
      break;
      
    case 1:
      // Blank all
      for(uint8_t i = 0; i < LedCount; i++) {
        pLeds[i] = CRGB::Black;
      }      
      break;
      
    case 2:
      // Set all to RGB 
      for(uint8_t i = 0; i < LedCount; i++) {
        pLeds[i].r = Arguments[0];
        pLeds[i].g = Arguments[1];
        pLeds[i].b = Arguments[2];
      }      
      break;      
      
    
    case 7:  // 0: Speed 0.1ms
      //Shot Like Effect
      brightness = 255;

      for(int i=0; i<LedCount; i++){
        pLeds[i] = CRGB::White;
      }
      Timestamp = micros();
      Storage32 = Arguments[0] * 100;
      Storage8[0] = 255;
      break;

    case 8:
      {
        //Fire Like Effect
        CRGBPalette16 currentPalette=LavaColors_p;
        brightness = 155;
        
        TBlendType    currentBlending = LINEARBLEND ;
        
        // Turn current LED on
        for(int i=0; i<LedCount; i++){
          pLeds[i] = ColorFromPalette( currentPalette, random(0, 255/LedCount*i), brightness, currentBlending);
            
        } 
      }
      break;    
  
    case 0x10:
      {
        // UFO animation
        CRGB color;
        color.r = Arguments[0];
        color.g = Arguments[1];
        color.b = Arguments[2];
        
        // Turn all LED on to color
        for(int i=0; i<LedCount; i++){
          pLeds[i] = color;  
        }      
        Timestamp = millis();
        Storage32 = 50;
        Storage8[0] = 0;
      }
      break;
  }  
}

void AnimElementClass::worker(void) {
  if(!pLeds || !LedCount) return;
  if(Flags & ANIFLAGBLANK) return;
  uint8_t brightness;
  TBlendType    currentBlending = LINEARBLEND ;
  CRGBPalette16 currentPalette=LavaColors_p;
  CRGB color;
  
  switch(EffectNumber) {
    case 0:
    case 1:
    case 2:
      // Do nothing.
      break;

    case 7:
      //Fire Like Effect - Use Arguments[0] to fade out
      
      
      if((micros() - Timestamp) > Storage32) {
        Timestamp += Storage32;
        if(Storage8[0] <= 0) {
          EffectNumber = 8;
        } else {
          Storage8[0]--;
        }
        brightness = Storage8[0];
        // Turn current LED on
        for(int i=0; i<LedCount; i++){
          pLeds[i] = ColorFromPalette( currentPalette, random(0, 255/LedCount*i), brightness, currentBlending);
            
        }        
      }

      break;  
      
    case 8:
      //Fire Like Effect

      brightness = 155;
      
      // Turn current LED on
      for(int i=0; i<LedCount; i++){
        pLeds[i] = ColorFromPalette( currentPalette, random(0, 255/LedCount*i), brightness, currentBlending);
          
      } 
      break;  
      
    case 0x10:
      // UFO animation
      if((millis() - Timestamp) > Storage32) {
        Timestamp += Storage32;

        color.r = Arguments[0];
        color.g = Arguments[1];
        color.b = Arguments[2];
      
        // Turn all LED on to color
        for(int i=0; i<LedCount; i++){
          pLeds[i] = color;  
        }      
        
        pLeds[(Storage8[0])%(LedCount-2)]   = CRGB::Black;
        pLeds[(Storage8[0]+1)%(LedCount-2)] = CRGB::White;
        pLeds[(Storage8[0]+2)%(LedCount-2)] = CRGB::Black;
  
        if(LedCount >= 26) {
          if((Storage8[0] % 6) == 0) {
            pLeds[24] = CRGB::White;
            pLeds[25] = CRGB::White;
          } else {
            pLeds[24] = CRGB::Black;
            pLeds[25] = CRGB::Black;        
          }
        }
        
        Storage8[0]++;
        
        if(Storage8[0]>=24) {
          Storage8[0] = 0;
          if(Arguments[3]) {
            Arguments[3]--;
            if(Arguments[3] == 0) { 
              EffectNumber = 0; 
              for(uint8_t i = 0; i < LedCount; i++) {
                pLeds[i] = CRGB::Black;
              }  
            }
          }          
        }
      }
      break;    
  
  }

}

// ********** MULTICLASS STUFF ****************

AnimClass::AnimClass(void) {

}

void AnimClass::worker(void) {
  for(int8_t i = 0; i < MAXANIMELM; i++) {
    AnimElm[i].worker();
  }
}

void AnimClass::shotMute(uint8_t onoff) {
  for(int8_t i = 0; i < MAXANIMELM; i++) {
    if(AnimElm[i].Flags & ANIFLAGSHOTBLANK) {
      AnimElm[i].mute(onoff);
    }
  }
}
