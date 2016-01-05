// Use if you want to force the software SPI subsystem to be used for some reason (generally, you don't)
// #define FORCE_SOFTWARE_SPI
// Use if you want to force non-accelerated pin access (hint: you really don't, it breaks lots of things)
// #define FORCE_SOFTWARE_SPI
// #define FORCE_SOFTWARE_PINS
#include "FastLED.h"

///////////////////////////////////////////////////////////////////////////////////////////
//
// Move a white dot along the strip of leds.  This program simply shows how to configure the leds,
// and then how to turn a single pixel white and then off, moving down the line of pixels.
// 

// How many leds are in the strip?
#define NUM_LEDS_RING 4

// Data pin that led data will be written out over
#define DATA_PIN 3

// Clock pin only needed for SPI based chipsets when not using hardware SPI
//#define CLOCK_PIN 8

// This is an array of leds.  One item for each led in your strip.
// CHSV leds[NUM_LEDS];
CRGB leds[NUM_LEDS_RING];
CHSV ledsHSV[NUM_LEDS_RING];

// This function sets up the ledsand tells the controller about them
void setup() {
	// sanity check delay - allows reprogramming if accidently blowing power w/leds
   	delay(2000);

      FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS_RING);
}

// This function runs over and over, and is where you do the magic to light
// your leds.

unsigned long timer_ufo_ring = 0UL;

long led_ramp_pos = 0L;

int ring_led_counter = 0;

long ledPos[3] = {0L,500L,1000L};


void loop() {
   unsigned long current_millis = millis();

   CHSV temp_hsv;

   bool requireLEDUpdate = false;
   

   if(timer_ufo_ring<current_millis) {
      timer_ufo_ring = current_millis+1L;

      led_ramp_pos+=1;

      for(int i=0; i<NUM_LEDS_RING-1; i++) {
         ledsHSV[i].h = 180; // 100
         ledsHSV[i].v =  255; // 128
         ledsHSV[i].s = 255-cubicwave8(max(min((led_ramp_pos%(192*3))-(i*192),255),0));
      }

      /*
      if(led_ramp_pos>192*3) {
         led_ramp_pos = 0;
      }
      */
      
      ledsHSV[3].h = 200;
      ledsHSV[3].s = 0; // tan(led_ramp_pos/3.141)*255; // random8();
      ledsHSV[3].v = (led_ramp_pos%50<20) && (led_ramp_pos%1000<200) ? 255:0; // ((led_ramp_pos | 0x3f) == 0x3f) ? 255 : 128;
      
      requireLEDUpdate = true;
   }

   if(requireLEDUpdate) showHSV(ledsHSV);
}

void showHSV(const struct CHSV * phsv) {
   CRGB *pLed;
   pLed = &leds[0];
   for(uint8_t i=0; i<NUM_LEDS_RING; i++) {
      hsv2rgb_rainbow(phsv[i], *pLed++);
   }
   FastLED.show();
}
