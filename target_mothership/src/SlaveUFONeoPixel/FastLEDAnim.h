/* 
 Copyright (c) 2015, Lutz Lisseck (lutz. lisseck AT gmx. de)
 
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
#ifndef __FASTLEDANIM_H__
#define __FASTLEDANIM_H__

#include <Arduino.h>
#include "FastLED.h"

#define MAXANIMELM    8

#define ANIFLAGSHOTBLANK  (1)
#define ANIFLAGBLANK      (2)


class AnimElementClass {
  private:
    uint8_t     EffectNumber;
    uint16_t    State;
    uint32_t    Timestamp;
    uint8_t     Storage8[2];
    uint32_t    Storage32;
    
  public:
    CRGB        *pLeds;   
    uint8_t     LedCount;

    uint8_t     Flags;          // Bit 0: If set object will be off while shot, Bit 1: muted
    
    uint8_t     Arguments[4];
    
    AnimElementClass(void);     // Constructor
    ~AnimElementClass(void);    // Destructor
    void        worker(void);    
    void        mute(uint8_t onoff);  // If true, blank object (animation internally continues)   
    void        startAnimation(uint8_t EffectNo);
    
};

class AnimClass {
  private:
  
  public: 
    AnimClass(void);     // Constructor
    AnimElementClass AnimElm[MAXANIMELM];
    
    void        worker(void);
    void        shotMute(uint8_t onoff);  // If true, blank objects if flag is set (animation internally continues)

};


#endif