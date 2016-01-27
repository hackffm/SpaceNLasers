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
#ifndef __LIGHTRX_H__
#define __LIGHTRX_H__

#include <Arduino.h>

#define MAXRXELM    8

class LightRxElementClass {
  private:
    uint8_t      Pin;            // Pin number
    uint8_t      Pullup;         // true: pullup on
  
  public:
    uint16_t     DarkValue;      // Last dark value read
    uint16_t     Threshold;      // Threshold for toggling bit
    uint8_t      Data;
    uint16_t     MaxValue;
    uint16_t     MinValue;
    
    LightRxElementClass(void);  // Constructor
    ~LightRxElementClass(void); // Destructor

    void        setPin(uint8_t analogPin, uint8_t pullupOn = 1);
    void        doReceiveBit(uint8_t state); // 0: darkread, 1-8 bit 0..7
};

class LightRxClass {
// don't change this struct from here ...

  private:
    void        doReceiveBitAll(uint8_t state);
    uint8_t     state;
    uint16_t    timestamp;
    
  public:
    LightRxClass(void);         // Constructor
    LightRxElementClass RxElm[MAXRXELM];
    uint16_t    bitTime;
    uint16_t    bitDelay;
    
    void        startReceive(void);     // Start the receiving
    uint8_t     doReceive(void);        // Call until this return 0    
};

#endif