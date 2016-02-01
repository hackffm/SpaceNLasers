// Use if you want to force the software SPI subsystem to be used for some reason (generally, you don't)
// #define FORCE_SOFTWARE_SPI
// Use if you want to force non-accelerated pin access (hint: you really don't, it breaks lots of things)
// #define FORCE_SOFTWARE_SPI
// #define FORCE_SOFTWARE_PINS
#include "FastLED.h"
#include "AnalogAnim.h"
#include "FastLEDAnim.h"

///////////////////////////////////////////////////////////////////////////////////////////
//
// Move a white dot along the strip of leds.  This program simply shows how to configure the leds,
// and then how to turn a single pixel white and then off, moving down the line of pixels.
// 

// How many leds are in the strip?
#define NUM_LEDS 7

// Data pin that led data will be written out over
#define DATA_PIN 3

#define MOTOR_PIN_A 9
#define MOTOR_PIN_B 10

// Clock pin only needed for SPI based chipsets when not using hardware SPI
//#define CLOCK_PIN 8

// This is an array of leds.  One item for each led in your strip.
// CHSV leds[NUM_LEDS];
CRGB leds[NUM_LEDS];
CHSV ledsHSV[NUM_LEDS];

byte ufoState = 0xFF;
unsigned long ufoTimer=0UL;

AnalogClass Analog;
AnimClass Anim;

uint8_t ufoMode;
uint8_t ufoArguments[10];
bool ufoStateChange = false;

// This function sets up the ledsand tells the controller about them
void setup() {
	// sanity check delay - allows reprogramming if accidently blowing power w/leds
	delay(2000);

	Serial.begin(2400);

	FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);

	ufoMode = 0;

	// default motor settings
	ufoArguments[5] = 204;
	ufoArguments[6] = 238;

	// ufo engine LEDs
	Anim.AnimElm[0].pLeds = leds;
	Anim.AnimElm[0].LedOffset = 0;
	Anim.AnimElm[0].LedCount = 3;

	// ufo cockpit LEDs
	Anim.AnimElm[1].pLeds = leds;
	Anim.AnimElm[1].LedOffset = 3;
	Anim.AnimElm[1].LedCount = 3;

	// ufo laser shot LED
	Anim.AnimElm[2].pLeds = leds;
	Anim.AnimElm[2].LedOffset = 6;
	Anim.AnimElm[2].LedCount = 1;
	
	// init virobi motor driver
	pinMode(MOTOR_PIN_A, OUTPUT);
	pinMode(MOTOR_PIN_B, OUTPUT);
	setPwmFrequency(MOTOR_PIN_A, 1);
	setPwmFrequency(MOTOR_PIN_B, 1);
	
	Analog.AnimElm[0].OutputID = MOTOR_PIN_A;
	Analog.AnimElm[0].Arguments[0] = 0;
	Analog.AnimElm[0].Arguments[1] = 0;
	Analog.AnimElm[0].Arguments[2] = MOTOR_PIN_A;
	Analog.AnimElm[0].Arguments[3] = MOTOR_PIN_B;
}

// This function runs over and over, and is where you do the magic to light
// your leds.

unsigned long timer_ufo_ring = 0UL;

long led_ramp_pos = 0L;

int ring_led_counter = 0;

long ledPos[3] = {0L,500L,1000L};


void loop() {
	unsigned long current_millis = millis();

	receive_serial_cmd();

	virobiUFOLoopNormalMode();

	virobiUFOLoopPanicMode();

	Anim.worker();
	Analog.worker();
	FastLED.show();
}


void receive_serial_cmd(void) {
	static uint8_t cmd[18];
	static uint8_t cmdcount = 0;
	uint8_t c;
	while(Serial.available()) {
		c = Serial.read();
		if(c > ' ') {
			cmd[cmdcount++] = c;
		}

		if((c == 8) && (cmdcount > 0)) cmdcount--;

		if((c == 0x0d) || (c == 0x0a) || (cmdcount > 16)) {
			cmd[cmdcount] = 0;
			if(cmdcount > 0) {
				switch(cmd[0]) {

					case 'a':  // NEOPIXEL Animation 
					// 1aONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
					if(cmdcount >= 4) {
						uint8_t objectNum = get1Hex(cmd[1]);
						uint8_t aniNum = get2Hex((char *)&cmd[2]);

						if(objectNum==0) { // main virobi ufo state object
							switch (aniNum) {
							    case 2:
							      // start ufo normal mode
							      	ufoMode = 0x01;
							      break;
							    case 0x09:
							      // start ufo panic mode
									ufoMode = 0x0A;
							      break;
							    default:
							    	ufoMode = 0x00;
							}
							// ufoMode = aniNum;
							ufoArguments[0] = get2Hex((char *)&cmd[4]); // BASE Color Red
							ufoArguments[1] = get2Hex((char *)&cmd[6]); // BASE Color Green
							ufoArguments[2] = get2Hex((char *)&cmd[8]); // BASE Color Blue

							ufoArguments[3] = get1Hex(cmd[9]); // Sec Move
							ufoArguments[4] = get1Hex(cmd[10]); // Sec Attack

							ufoStateChange = true;
						}

						if(objectNum>0 && objectNum < MAXANIMELM+1) { // if(objectNum>=8) {
							objectNum = objectNum-1;
							if(cmdcount >= 5) {
								Anim.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[4]);
							}
							if(cmdcount >= 7) {
								Anim.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[6]);
							}
							if(cmdcount >= 9) {
								Anim.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[8]);
							}
							if(cmdcount >= 11) {
								Anim.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[10]);
							}
							Anim.AnimElm[objectNum].startAnimation(aniNum);
							Serial.println(Anim.AnimElm[objectNum].Arguments[3]);
						}
					}
					break;

					case 'A':  // Analog Animation 
					// 1AONN AABBCCDD O = Objekt Nummer, NN = Animation number (Hex), AABBCCDD (Hex, optionales Argument)
					if(cmdcount >= 4) {
						uint8_t objectNum = get1Hex(cmd[1]);
						uint8_t aniNum = get2Hex((char *)&cmd[2]);
						/*
						if(objectNum < MAXANALOGELM) { // if(objectNum==4) {
							// objectNum = objectNum - 4;
							if(cmdcount >= 5) {
								Analog.AnimElm[objectNum].Arguments[0] = get2Hex((char *)&cmd[4]);
							}
							if(cmdcount >= 7) {
								Analog.AnimElm[objectNum].Arguments[1] = get2Hex((char *)&cmd[6]);
							}
							if(cmdcount >= 9) {
								Analog.AnimElm[objectNum].Arguments[2] = get2Hex((char *)&cmd[8]);
							}
							if(cmdcount >= 11) {
								Analog.AnimElm[objectNum].Arguments[3] = get2Hex((char *)&cmd[10]);
							}                    
							Analog.AnimElm[objectNum].startAnimation(aniNum);
						}
						*/

						// UFO Config
						if(objectNum==0 && cmdcount>=8) {
							ufoArguments[5] = get2Hex((char *)&cmd[4]); // Speed Normal Move
							ufoArguments[6] = get2Hex((char *)&cmd[6]); // Speed Hit
						}

						// UFO Sequence parser
						if(objectNum==1 && cmdcount>=9) {
							ufoMode = aniNum;
							ufoArguments[0] = get2Hex((char *)&cmd[4]); // BASE Color Red
							ufoArguments[1] = get2Hex((char *)&cmd[6]); // BASE Color Green
							ufoArguments[2] = get2Hex((char *)&cmd[8]); // BASE Color Blue

							ufoArguments[3] = get1Hex(cmd[9]); // Sec Move
							ufoArguments[4] = get1Hex(cmd[10]); // Sec Attack

							ufoStateChange = true;
							
						}
						// Serial.println(cmdcount);
					}
					break;

					// motor einstellung
					// activieren / deactivieren
					// treffer animation
					// basis farbe aendern
					// [o] ufo attack
				}
			}

			cmdcount = 0;
		}
	}
}  

byte ufoTurn = 0;

void virobiUFOLoopNormalMode() {
	switch (ufoMode) { // UFO Statemachine
		case 0x00: // ufo disable state
			Analog.AnimElm[0].Arguments[0] = 0x00;
			Analog.AnimElm[0].Arguments[1] = 0x00;
			Analog.AnimElm[0].startAnimation(0x30);

			Anim.AnimElm[0].Arguments[0] = 0xFF;
			Anim.AnimElm[0].Arguments[1] = 0x00;
			Anim.AnimElm[0].Arguments[2] = 0x00;
			// Anim.AnimElm[0].Arguments[3] = 0x05;
			Anim.AnimElm[0].startAnimation(2);

			// Anim.AnimElm[1].startAnimation(0x01);
			Anim.AnimElm[1].Arguments[0] = 0xAA;
			Anim.AnimElm[1].Arguments[1] = 0x00;
			Anim.AnimElm[1].Arguments[2] = 0x0F;
			Anim.AnimElm[1].Arguments[3] = 0x01;
			Anim.AnimElm[1].startAnimation(0x0A);

			Anim.AnimElm[2].startAnimation(0x01);
			ufoMode = 0x10;
		  	ufoTimer = millis() + 1000UL;
			break;
		case 0x10: // ufo disable state refresh
			if(millis()>ufoTimer) {
				ufoMode = 0x00;
		  		Anim.AnimElm[0].Arguments[0] = 0xFF;
				Anim.AnimElm[0].Arguments[1] = 0x00;
				Anim.AnimElm[0].Arguments[2] = 0x00;
				// Anim.AnimElm[0].Arguments[3] = 0x05;
				Anim.AnimElm[0].startAnimation(2);
			}
			break;
			/*
		case 0x11:
			if(millis()>ufoTimer) {
				ufoMode = 0x00;
			}
			break;
		*/
		case 0x01:	// start normal mode loop
			Anim.AnimElm[0].Arguments[0] = 0x77;
			Anim.AnimElm[0].Arguments[1] = 0x44;
			Anim.AnimElm[0].Arguments[2] = 0xFF;
			Anim.AnimElm[0].Arguments[3] = 0x02;
			Anim.AnimElm[0].startAnimation(0x0A);

			Anim.AnimElm[1].Arguments[0] = ufoArguments[0];
			Anim.AnimElm[1].Arguments[1] = ufoArguments[1];
			Anim.AnimElm[1].Arguments[2] = ufoArguments[2];
			Anim.AnimElm[1].Arguments[3] = 0x02;
			Anim.AnimElm[1].startAnimation(0x0A);

			if(ufoTurn>3) {
				Analog.AnimElm[0].Arguments[0] = 0x00;
				Analog.AnimElm[0].Arguments[1] = ufoArguments[5];
				Analog.AnimElm[0].startAnimation(0x30);	
				ufoTurn = 0;
			} else {
				Analog.AnimElm[0].Arguments[0] = ufoArguments[5];
				Analog.AnimElm[0].Arguments[1] = 0x00;
				Analog.AnimElm[0].startAnimation(0x30);	
			}

			ufoTurn++;
			
		  	ufoMode = 0x02;
		  	ufoTimer = millis() + 2000UL;
			break;
		case 0x02:
			if(millis()>ufoTimer) {
				ufoMode = 0x03;
			}
			// Serial.println("0x02");
			break;
		case 0x03:
			Analog.AnimElm[0].Arguments[0] = 0x00;
			Analog.AnimElm[0].Arguments[1] = 0x00;
			Analog.AnimElm[0].startAnimation(0x30);

			Anim.AnimElm[2].Arguments[0] = 0xFF;
			Anim.AnimElm[2].Arguments[1] = 0xFF;
			Anim.AnimElm[2].Arguments[2] = 0xFF;
			Anim.AnimElm[2].Arguments[3] = 0x05;
			Anim.AnimElm[2].startAnimation(0x09);

			ufoMode = 0x04;
			
			ufoTimer = millis() + 4000UL;
			break;
		case 0x04:
			if(millis()>ufoTimer) {
				ufoMode = 0x05;
			}
			// Serial.println("0x04");
			break;
		case 0x05:
			Anim.AnimElm[2].Arguments[0] = 0x00;
			Anim.AnimElm[2].Arguments[1] = 0x00;
			Anim.AnimElm[2].Arguments[2] = 0x00;
			Anim.AnimElm[2].Arguments[3] = 0x05;
			Anim.AnimElm[2].startAnimation(0x09);
			ufoMode = 0x01;
			
			break;
		default:
		  // do something
			break;
	}
}

void virobiUFOLoopPanicMode() {
	switch (ufoMode) { // UFO Statemachine
		case 0x0A: // panik mode start
			// Serial.println("0x01");
			Analog.AnimElm[0].Arguments[0] = ufoArguments[6];
			Analog.AnimElm[0].Arguments[1] = 0x00;
			Analog.AnimElm[0].startAnimation(0x30);

			Anim.AnimElm[0].Arguments[0] = 0xFF;
			Anim.AnimElm[0].Arguments[1] = 0x00;
			Anim.AnimElm[0].Arguments[2] = 0x00;
			Anim.AnimElm[0].Arguments[3] = 0x04;
			Anim.AnimElm[0].startAnimation(0x09);

			Anim.AnimElm[1].Arguments[0] = 0xFF;
			Anim.AnimElm[1].Arguments[1] = 0x00;
			Anim.AnimElm[1].Arguments[2] = 0x00;
			Anim.AnimElm[1].Arguments[3] = 0x02;
			Anim.AnimElm[1].startAnimation(0x09);

			Anim.AnimElm[2].Arguments[0] = 0x00;
			Anim.AnimElm[2].Arguments[1] = 0x00;
			Anim.AnimElm[2].Arguments[2] = 0x00;
			Anim.AnimElm[2].Arguments[3] = 0x05;
			Anim.AnimElm[2].startAnimation(0x09);
		  	ufoMode = 0x0B;
		  	ufoTimer = millis() + 5000UL;
		  	
			break;
		case 0x0B:
			if(millis()>ufoTimer) {
				ufoMode = 0x0C;
			}
			break;
		case 0x0C:
			Analog.AnimElm[0].Arguments[0] = 0x00;
			Analog.AnimElm[0].Arguments[1] = 0x00;
			Analog.AnimElm[0].startAnimation(0x30);

			Anim.AnimElm[0].Arguments[0] = 0x77;
			Anim.AnimElm[0].Arguments[1] = 0x44;
			Anim.AnimElm[0].Arguments[2] = 0xFF;
			Anim.AnimElm[0].Arguments[3] = 0x02;
			Anim.AnimElm[0].startAnimation(0x0A);

			Anim.AnimElm[1].Arguments[0] = ufoArguments[0];
			Anim.AnimElm[1].Arguments[1] = ufoArguments[1];
			Anim.AnimElm[1].Arguments[2] = ufoArguments[2];
			Anim.AnimElm[1].Arguments[3] = 0x02;
			Anim.AnimElm[1].startAnimation(0x0A);

			ufoTimer = millis() + 500UL;

			ufoMode = 0x0D;
			break;

		case 0x0D:
			if(millis()>ufoTimer) {
				ufoMode = 0x01;
			}
			break;
	}
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


void showHSV(const struct CHSV * phsv) {
	CRGB *pLed;
	pLed = &leds[0];
	for(uint8_t i=0; i<NUM_LEDS; i++) {
		hsv2rgb_rainbow(phsv[i], *pLed++);
	}
	FastLED.show();
}

void setPwmFrequency(int pin, int divisor) {
	byte mode;
	if(pin == 5 || pin == 6 || pin == 9 || pin == 10) {
		switch(divisor) {
			case 1: mode = 0x01; break;
			case 8: mode = 0x02; break;
			case 64: mode = 0x03; break;
			case 256: mode = 0x04; break;
			case 1024: mode = 0x05; break;
			default: return;
		}
		if(pin == 5 || pin == 6) {
			TCCR0B = TCCR0B & 0b11111000 | mode;
		} else {
			TCCR1B = TCCR1B & 0b11111000 | mode;
		}
	} else if(pin == 3 || pin == 11) {
		switch(divisor) {
			case 1: mode = 0x01; break;
			case 8: mode = 0x02; break;
			case 32: mode = 0x03; break;
			case 64: mode = 0x04; break;
			case 128: mode = 0x05; break;
			case 256: mode = 0x06; break;
			case 1024: mode = 0x7; break;
			default: return;
		}
		TCCR2B = TCCR2B & 0b11111000 | mode;
  }
}
