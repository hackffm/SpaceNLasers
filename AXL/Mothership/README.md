# Space'n'Lasers - Mothership

## Firmware commands

### Synchronous
|Command|Identifier|Parameter|Return|Comment|
|---|---|---|---|---|
|Identify|i|n/a|Identify string, example: homeposition, speed, acceleration
|Halt|h|n/a|k...|using the current speed & acceleration limits|
|Move|m|position
|Home|H|n/a|k...|Sets current position to home position = 0 (zero)
|Set speed|s|steps/sec|k...|in steps/second (unreliable > 1000)
|Set acceleration|a|steps/sec/sec|k...|in steps/second²
|Wait|w|milliseconds|k...|just waits
|debug home|z|n/a|State of the home switch

### Asynchronous
    d;*cmd*;*position*

## Messungen 22.12.2015
* Mothership in HackFFM
* Large roll for windows blinds
* Half steps
* Stepper 200 steps

|Steps|mm distance|
|---|---|
|0|0|
|1000|335|
|2000|670|
|3000|1001|


## Momentary switch for home position

* for Arduino digital input
* pull-up resistor 10k - open swich = +Vcc / 5V

```
PIN               ,_____,
(1)       +5V O---| 10k |---'   pull-up resistor
                  '~~~~~'   |
(2)    Signal O-------------O
                            |
(3)       n/a O              /  momentary switch
                            |
(4)       GND O-------------'
```

## Pinout for stepper motor

|Pin|Name|Color|
|---|---|---|
|1|2A|![][106] Blue|
|2|2B|![][102] Red|
|3|1B|![][100] Black|
|4|1A|![][105] Green|




  [100]: http://www.realaxl.de/static/pix/color_gadgets/square_16_black.png
  [101]: http://www.realaxl.de/static/pix/color_gadgets/square_16_brown.png
  [102]: http://www.realaxl.de/static/pix/color_gadgets/square_16_red.png
  [103]: http://www.realaxl.de/static/pix/color_gadgets/square_16_orange.png
  [104]: http://www.realaxl.de/static/pix/color_gadgets/square_16_yellow.png
  [105]: http://www.realaxl.de/static/pix/color_gadgets/square_16_green.png
  [106]: http://www.realaxl.de/static/pix/color_gadgets/square_16_blue.png
  [107]: http://www.realaxl.de/static/pix/color_gadgets/square_16_purple.png
  [108]: http://www.realaxl.de/static/pix/color_gadgets/square_16_grey.png
  [109]: http://www.realaxl.de/static/pix/color_gadgets/square_16_white.png
  [110]: http://www.realaxl.de/static/pix/color_gadgets/square_16_gold.png  