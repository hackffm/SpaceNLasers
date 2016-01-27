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
#ifndef __LIGHTTX_H__
#define __LIGHTTX_H__

#include <Arduino.h>

#define MAXTXELM    3

class LightTxElementClass {
  private:
    uint8_t     Pin;            // Pin number
  
  public:
    uint8_t     Visible;        // PWM value >0 to make laser visible
    uint8_t     Data;
    uint8_t     Enabled;        // Only send if !0
    
    LightTxElementClass(void);   // Constructor
    ~LightTxElementClass(void);  // Destructor

    void        setPin(uint8_t laserPin, uint8_t visiValue = 0);
    void        setVisible(uint8_t visiValue);  // don't use this while shot is beeing transmitted
    void        doTransmitBit(uint8_t state);   // 0: darkread, 1-8 bit 0..7, 9 done
};

class LightTxClass {
// don't change this struct from here ...

  private:
    void        doTransmitBitAll(uint8_t state);
    uint8_t     shotTriggered;
    uint8_t     state;
    uint16_t    timestamp;
    
  public:
    LightTxClass(void);         // Constructor
    LightTxElementClass TxElm[MAXTXELM];
    uint16_t    bitTime;
    
    void        triggerShot(void);      // Fires a shot in next transmit stage
    
    void        startTransmit(void);    // Start the transmitting
    uint8_t     doTransmit(void);       // Call until this return 0
};

#endif