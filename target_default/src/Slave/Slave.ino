/*

 0 RxD
 1 TxD
 2 TxEN

*/

//#define I_AM_WEAPON    1
#define I_AM_TARGET    1
//#define I_AM_UFO       1

#include <EEPROM.h>
#include "FastLED.h"
#include "LightRx.h"
#include "LightTx.h"
#include "FastLEDAnim.h"
#include "AnalogAnim.h"

uint8_t  ownID = 0xff;
uint8_t  IDRWEnable = 0;        // If set to 0xaa ID can be read an write
uint8_t  FeuerFrei = 0;         // Wenn !0, dann darf das Device beim nächsten Schuss-Befehl schießen.
uint8_t  ShotReady = 0;         // Wenn !0, Lichter ggf. aus und auf Schuss warten
uint16_t ShotBitTime = 500;     // per bit in uS

#define TXEN   2
#define IDWRITEENABLE A0            // if connected to D13 at startup ID read write is enabled

#ifdef I_AM_WEAPON
  LightTxClass LightTx;
  #define MUZZLEFLARE 8 
  #define LIGHTSHOW 9 
  
  #define RUMBLE 5 
  
  #define LOADBUTTON 7 
  #define FIREBUTTON 4   
  #define THUMBBUTTON 10
  
  #define BARREL 3      // INT1
  volatile uint8_t BarrelIntCount = 0;
  
  #define LAZOR_TX   6 
  #define SHOTGUN_TX 12  
  
  //defining LED stuff
  #define NUM_LEDS_SHOW 6
  CRGB leds_show[NUM_LEDS_SHOW];
  #define NUM_LEDS_MUZZLE 1
  CRGB leds_muzzle[NUM_LEDS_MUZZLE];  
  
  #define WEAPON_A_TXID   (0x91)
  #define WEAPON_B_TXID   (0xA2)
#endif

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
  Serial.begin(38400);
  ownID = EEPROM.read(0x03);
  if (EEPROM.read(0x04) != (ownID ^ 0xAA)) ownID = 0xff;
  
  pinMode(TXEN, OUTPUT);
  digitalWrite(TXEN, LOW);
  checkIDWriteEnable();
  if(ownID == 0xff) IDRWEnable = 0xaa;
  
  pinMode(13, OUTPUT);
  pinMode(10, OUTPUT);
  
  #ifdef I_AM_WEAPON
    LightTx.TxElm[0].setPin(LAZOR_TX, 25);
    LightTx.TxElm[0].Enabled = 1;  
    LightTx.TxElm[1].setPin(SHOTGUN_TX, 0);
    LightTx.TxElm[1].Enabled = 1;    
    LightTx.TxElm[0].Data = (ownID == 'A')?WEAPON_A_TXID:WEAPON_B_TXID;
    LightTx.TxElm[1].Data = LightTx.TxElm[0].Data | 0x04;
    
    //Pin Modes
    pinMode(LOADBUTTON, INPUT_PULLUP);
    pinMode(FIREBUTTON, INPUT_PULLUP);
    pinMode(THUMBBUTTON, INPUT_PULLUP);

    pinMode(BARREL, INPUT_PULLUP);
    attachInterrupt(1, BarrelInterrupt, RISING);    
    
    FastLED.addLeds<NEOPIXEL, LIGHTSHOW>(leds_show, NUM_LEDS_SHOW);
    FastLED.addLeds<NEOPIXEL, MUZZLEFLARE>(leds_muzzle, NUM_LEDS_MUZZLE); 
    Anim.AnimElm[0].pLeds = leds_show;
    Anim.AnimElm[0].LedCount = NUM_LEDS_SHOW;
    Anim.AnimElm[1].pLeds = leds_muzzle;
    Anim.AnimElm[1].LedCount = NUM_LEDS_MUZZLE;  

    pinMode(RUMBLE, OUTPUT);
    Analog.AnimElm[0].OutputID = RUMBLE;
    Analog.AnimElm[0].directSet(0);  

    Analog.AnimElm[1].pAnalogSet = setMainLaser;
    Analog.AnimElm[1].directSet(0);    
  #endif
  
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
        Anim.AnimElm[i].pLeds[0] = CRGB::Black;
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

      FastLED.show();
      for(int i=0; i<8; i++) {
        Anim.AnimElm[i].pLeds[0] = CRGB::White;
        FastLED.show();
        delay(100);
      }
      delay(2000);
      for(int i=0; i<8; i++) {
        Anim.AnimElm[i].pLeds[0] = CRGB::Black;
        FastLED.show();
        delay(100);
      }      
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
      //digitalWrite(13, !digitalRead(13));
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
        case 'S':  // Schuss-Sequenz starten 
          #ifdef I_AM_WEAPON
          LightTx.startTransmit();
          #endif
          #ifdef I_AM_TARGET
          LightRx.startReceive();
          #endif
          {
            uint8_t notDone = 1;
            while(notDone) {
              notDone = 0;
              #ifdef I_AM_WEAPON
              notDone += LightTx.doTransmit();
              #endif
              #ifdef I_AM_TARGET
              notDone += LightRx.doReceive();
              #endif              
            }
          }
          ShotReady = 0;
          FeuerFrei = 0;
          Anim.shotMute(0);
          Analog.shotMute(0);
          #ifdef I_AM_WEAPON
            txEn();
            Serial.write('x');
            txDis();
          #endif
          break;          
        
        case 's':  // Bereit machen für Schuss, Waffe aktiv schalten     
          ShotReady = 1;
          // Teste ob geschossen werden darf.
          for(uint8_t i=1; i<cmdcount; i++) {
            if(cmd[i] == ownID) {
              FeuerFrei = 1;
              Anim.shotMute(1); FastLED.show();
              Analog.shotMute(1);
              #ifdef I_AM_WEAPON
              LightTx.triggerShot();
              #endif
            }
          }
          break;          
        
        case 'I':
          if((IDRWEnable == 0xaa) && (cmdcount == 3) && (cmd[1] == cmd[2])) {
            EEPROM.write(0x03, cmd[1]);
            EEPROM.write(0x04, cmd[1] ^ 0xaa);
            ownID = cmd[1];
            txEn();
            Serial.print(F("Wrote "));
            Serial.write(ownID);
            Serial.write(0x0d);
            Serial.write(0x0a);
            txDis();            
          } else if(((IDRWEnable == 0xaa) && (cmdcount == 1)) || (cmdcount == 2)) {  
            txEn();
            Serial.print(F("My ID: "));
            Serial.write(ownID);
            Serial.write(' ');
            Serial.print(IDRWEnable, HEX);
            Serial.write(0x0d);
            Serial.write(0x0a);
            txDis(); 
          } 
          break; 
            

        case 'f':
          if(cmdcount > 9) {
            uint16_t a, b;
            a = ((uint16_t)get2Hex((char *)&cmd[1]))<<8 | (uint16_t)get2Hex((char *)&cmd[3]);
            b = ((uint16_t)get2Hex((char *)&cmd[5]))<<8 | (uint16_t)get2Hex((char *)&cmd[7]);
            print4Hex(a);
            print4Hex(b); 
            #ifdef I_AM_TARGET
            LightRx.bitTime = a;
            LightRx.bitDelay = b;
            #endif
            #ifdef I_AM_WEAPON
            LightTx.bitTime = a;
            #endif
          }                    
          break;  

        case 'T':
          if((cmdcount > 2) && (cmdcount < 7)) {
            unsigned int temp = atoi((const char *)&cmd[1]);           
            Serial.print("Th:");
            Serial.println(temp); 
            #ifdef I_AM_TARGET
            for(int j=0;j<8;j++) {
              LightRx.RxElm[j].Threshold = temp;
            }
            #endif
          }                    
          break;           

        default:
          if((cmd[0] == ownID) && (cmdcount >= 2)) {
            
            switch(cmd[1]) {
              case 'd': // debug
                if((cmdcount > 1)) {
                  txEn();
                  Serial.write(ownID);
                  Serial.write(0x0d);
                  Serial.write(0x0a);
                  #ifdef I_AM_TARGET
                  for(int i=0; i<MAXRXELM; i++) {
                    Serial.print(LightRx.RxElm[i].DarkValue);
                    Serial.write(' ');
                    Serial.print(LightRx.RxElm[i].Threshold);
                    Serial.write(' ');
                    Serial.print(LightRx.RxElm[i].Data);
                    Serial.write(' ');
                    Serial.print(LightRx.RxElm[i].MaxValue);
                    Serial.write(' ');
                    Serial.println(LightRx.RxElm[i].MinValue);                
                  }
                  #endif
                  txDis();
                }
                break;
                
              case 'b':  // button & Co. status
                #ifdef I_AM_WEAPON
                {
                  uint8_t buttonState = 0;
                  if(!digitalRead(FIREBUTTON))  buttonState |= 1;
                  if(!digitalRead(LOADBUTTON))  buttonState |= 2;
                  if(!digitalRead(THUMBBUTTON)) buttonState |= 4;
                  if(!digitalRead(BARREL))      buttonState |= 8;
                  txEn();
                  print2Hex(buttonState);
                  print2Hex(getBarrelCount());              
                  txDis();
                }
                #endif
                break;
                
              case 'a':  // NEOPIXEL Animation 
                // 1aONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
                if(cmdcount >= 5) {
                  uint8_t objectNum = get1Hex(cmd[2]);
                  uint8_t aniNum = get2Hex((char *)&cmd[3]);
                  if(objectNum < MAXANIMELM) {
                    if(cmdcount >= 7) {
                      Anim.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[5]);
                    }
                    if(cmdcount >= 9) {
                      Anim.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[7]);
                    }
                    if(cmdcount >= 11) {
                      Anim.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[9]);
                    }
                    if(cmdcount >= 13) {
                      Anim.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[11]);
                    }                    
                    Anim.AnimElm[objectNum].startAnimation(aniNum);
                    // Serial.print(objectNum);
                    // Serial.write(' ');
                    // Serial.print(aniNum);
                    // Serial.write(' '); 
                    // Serial.print(Anim.AnimElm[objectNum].Arguments[3]);
                  }
                }
                break;
                
              case 'A':  // Analog Animation 
                // 1AONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
                if(cmdcount >= 5) {
                  uint8_t objectNum = get1Hex(cmd[2]);
                  uint8_t aniNum = get2Hex((char *)&cmd[3]);
                  if(objectNum < MAXANALOGELM) {
                    if(cmdcount >= 7) {
                      Analog.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[5]);
                    }
                    if(cmdcount >= 9) {
                      Analog.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[7]);
                    }
                    if(cmdcount >= 11) {
                      Analog.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[9]);
                    }
                    if(cmdcount >= 13) {
                      Analog.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[11]);
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
                
              case 't': // target query
                #ifdef I_AM_TARGET
                if((cmdcount == 2) || ((cmdcount > 2) && (cmd[2] == 'r'))) {
                  txEn();
                  for(int i=0; i<MAXRXELM; i++) {
                    print2Hex(LightRx.RxElm[i].Data);   
                    LightRx.RxElm[i].Data = 0;             
                  }
                  txDis();
                } else if(cmdcount > 2) {
                  uint8_t obj = get1Hex(cmd[2]);
                  if(obj < MAXRXELM) {
                    txEn();
                    print2Hex(LightRx.RxElm[obj].Data);
                    Serial.write(' ');
                    print4Hex(LightRx.RxElm[obj].DarkValue);
                    Serial.write(' ');
                    print4Hex(LightRx.RxElm[obj].MinValue);
                    Serial.write(' ');
                    print4Hex(LightRx.RxElm[obj].MaxValue);
                    Serial.write(' ');
                    print4Hex(LightRx.RxElm[obj].Threshold);
                    LightRx.RxElm[obj].Data = 0;
                    txDis();
                  }
                }
                #endif
                break;

                
              case 'T': // threshold set
                #ifdef I_AM_TARGET
                if(cmdcount >= 6) {
                  uint16_t t = ((uint16_t)get2Hex((char *)&cmd[2]))<<8 | get2Hex((char *)&cmd[4]);
                  for(int i=0; i<MAXRXELM; i++) {
                    LightRx.RxElm[i].Threshold = t;                
                  }
                } 
                #endif
                break;                 
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
