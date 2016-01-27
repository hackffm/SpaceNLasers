/*

 0 RxD
 1 TxD
 2 TxEN

*/

// #define I_AM_WEAPON    1
#define I_AM_TARGET    1
#define I_AM_UFO       1

#include "FastLED.h"
#include "LightRx.h"
#include "LightTx.h"
#include "FastLEDAnim.h"
#include "AnalogAnim.h"

uint8_t  IDRWEnable = 0;        // If set to 0xaa ID can be read an write
uint8_t  FeuerFrei = 0;         // Wenn !0, dann darf das Device beim nächsten Schuss-Befehl schießen.
uint8_t  ShotReady = 0;         // Wenn !0, Lichter ggf. aus und auf Schuss warten
uint16_t ShotBitTime = 500;     // per bit in uS

#define TXEN   2
#define IDWRITEENABLE A0            // if connected to D13 at startup ID read write is enabled


#ifdef I_AM_TARGET
  LightRxClass LightRx;
  #ifdef I_AM_UFO
    #define UFO_LED_COUNT 26
    #define NUM_TARGET_LEDS (UFO_LED_COUNT + 6)
  #else
    #define NUM_TARGET_LEDS 8
  #endif
  CRGB targetLeds[NUM_TARGET_LEDS];
#endif

AnimClass Anim;
AnalogClass Analog;

void setup() {
  Serial.begin(2400);

  
  pinMode(TXEN, OUTPUT);
  digitalWrite(TXEN, LOW);
  
  pinMode(13, OUTPUT);
  pinMode(10, OUTPUT);
  
  
  #ifdef I_AM_TARGET
    LightRx.RxElm[0].setPin(A0,0);
    LightRx.RxElm[1].setPin(A1,0);
    LightRx.RxElm[2].setPin(A2,0);
    LightRx.RxElm[3].setPin(A3,0); 
    LightRx.RxElm[4].setPin(A4,0);
    LightRx.RxElm[5].setPin(A5,0);
    LightRx.RxElm[6].setPin(A6,0);
    LightRx.RxElm[7].setPin(A7,0);  
    
    #if I_AM_UFO
      // UFO only one strip on pin 4
      Anim.AnimElm[0].pLeds = targetLeds;
      Anim.AnimElm[0].LedCount = UFO_LED_COUNT; 
      FastLED.addLeds<NEOPIXEL, 4>(targetLeds+0, UFO_LED_COUNT); 
    #else
      // Target LEDs typical on 4,5,6,7,8,11,12,13   
      uint8_t pix[] = { 4,5,6,7,8,11,12,13 };
      for(int i=0; i<8; i++) {
        Anim.AnimElm[i].pLeds = targetLeds+i;
        Anim.AnimElm[i].LedCount = 1; 
      }    
      FastLED.addLeds<NEOPIXEL, 4>(targetLeds+0, 1);     
      FastLED.addLeds<NEOPIXEL, 5>(targetLeds+1, 1);
      FastLED.addLeds<NEOPIXEL, 6>(targetLeds+2, 1);
      FastLED.addLeds<NEOPIXEL, 7>(targetLeds+3, 1);
      FastLED.addLeds<NEOPIXEL, 8>(targetLeds+4, 1);
      FastLED.addLeds<NEOPIXEL,11>(targetLeds+5, 1);
      FastLED.addLeds<NEOPIXEL,12>(targetLeds+6, 1);
      FastLED.addLeds<NEOPIXEL,13>(targetLeds+7, 1);
    #endif
    
    // PWM's 3,9,10 
    pinMode(3, OUTPUT);
    Analog.AnimElm[0].OutputID = 3;
    Analog.AnimElm[0].directSet(0);  
    
    pinMode(9, OUTPUT);
    Analog.AnimElm[1].OutputID = 9;
    Analog.AnimElm[1].directSet(0); 

    pinMode(10, OUTPUT);
    Analog.AnimElm[2].OutputID = 10;
    Analog.AnimElm[2].directSet(0);
  #endif

}

void loop() {
  static uint16_t blink1 = millis();
  // put your main code here, to run repeatedly:
  receive_serial_cmd();
  
  if(!ShotReady) {
    Anim.worker();
    Analog.worker();
    FastLED.show();
    if(((uint16_t)(millis()) - blink1) > 1000) {
      blink1 = millis();
      digitalWrite(13, !digitalRead(13));
    }
  }
}

void receive_serial_cmd(void) {
  static uint8_t cmd[18];
  static uint8_t cmdcount = 0;
  uint8_t c;
  while(Serial.available()) {
    c = Serial.read();
    if(c > ' ') cmd[cmdcount++] = c;
    if((c == 8) && (cmdcount > 0)) cmdcount--;
    if((c == 0x0d) || (c == 0x0a) || (cmdcount > 16)) {
      cmd[cmdcount] = 0;
      if(cmdcount > 0) {
            
            switch(cmd[0]) {

              case 'a':  // NEOPIXEL Animation 
                // 1aONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
                if(cmdcount >= 5) {
                  uint8_t objectNum = get1Hex(cmd[1]);
                  uint8_t aniNum = get2Hex((char *)&cmd[2]);
                  if(objectNum==8) {
                    objectNum = 0;
                    if(cmdcount >= 6) {
                      Anim.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[4]);
                    }
                    if(cmdcount >= 8) {
                      Anim.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[6]);
                    }
                    if(cmdcount >= 10) {
                      Anim.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[8]);
                    }
                    if(cmdcount >= 12) {
                      Anim.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[10]);
                    }                    
                    Anim.AnimElm[objectNum].startAnimation(aniNum);
                    //Serial.print(objectNum);
                    //Serial.write(' ');
                    //Serial.print(aniNum);
                    //Serial.write(' '); 
                    //Serial.print(Anim.AnimElm[objectNum].Arguments[0]);
                  }
                }
                break;
                
              case 'A':  // Analog Animation 
                // 1AONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
                if(cmdcount >= 5) {
                  uint8_t objectNum = get1Hex(cmd[1]);
                  uint8_t aniNum = get2Hex((char *)&cmd[2]);
                  if(objectNum < MAXANALOGELM) {
                    if(cmdcount >= 6) {
                      Analog.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[4]);
                    }
                    if(cmdcount >= 8) {
                      Analog.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[6]);
                    }
                    if(cmdcount >= 10) {
                      Analog.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[8]);
                    }
                    if(cmdcount >= 12) {
                      Analog.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[10]);
                    }                    
                    Analog.AnimElm[objectNum].startAnimation(aniNum);
                    //Serial.print(objectNum);
                    //Serial.write(' ');
                    //Serial.print(aniNum);
                    //Serial.write(' '); 
                    //Serial.print(Analog.AnimElm[objectNum].Arguments[0]);
                  }
                }
                break;
                
                          
            }

          

      }
      cmdcount = 0;
    }
    
  }
}  

void print4Hex(uint16_t val) {
  print2Hex((uint8_t)(val >> 8));
  print2Hex((uint8_t)(val & 0xff));
}

void print2Hex(const uint8_t val) {
  if(val<=0x0f) Serial.write('0');
  Serial.print(val,HEX);
} 

// convert single hex digit to value
uint8_t get1Hex(const char b) {
  uint8_t ret = 0;
  if((b >= '0') && (b <= '9')) {
    ret = b - '0';
  } else if((b >= 'a') && (b <= 'f')) {
    ret = b - 'a' + 10;
  } else if((b >= 'A') && (b <= 'F')) {
    ret = b - 'A' + 10;
  }
  return ret;
} 

// convert double hex digit to value
uint8_t get2Hex(char *b) {
  uint8_t ret = 0;
  ret = get1Hex(b[0]);
  ret <<= 4;
  ret |= get1Hex(b[1]);
  return ret;
}

void txEn() {
  digitalWrite(TXEN, HIGH);
  delayMicroseconds(10);
}

void txDis() {
  Serial.write(0x0d);
  Serial.write(0x0a);
  Serial.flush();
  digitalWrite(TXEN, LOW);
}

void checkIDWriteEnable() {
  pinMode(IDWRITEENABLE, INPUT_PULLUP);
  pinMode(13, OUTPUT);
  IDRWEnable = 0;
  uint8_t id = 0xaa;
  for(uint8_t i = 0; i < 8; i++) {
    digitalWrite(13, (id & (1<<i))?HIGH:LOW);
    delayMicroseconds(4);
    IDRWEnable |= digitalRead(IDWRITEENABLE)?(1<<i):0;
  }
}

#ifdef I_AM_WEAPON
void BarrelInterrupt(void) {
  BarrelIntCount++;
}   

uint8_t getBarrelCount(void) {
  uint8_t ret;
  noInterrupts();
  ret = BarrelIntCount;
  BarrelIntCount = 0;
  interrupts();
  return(ret);
}

void setMainLaser(uint8_t id, uint8_t value) {
  LightTx.TxElm[0].setVisible(value);
  //print2Hex(value);
}
#endif
