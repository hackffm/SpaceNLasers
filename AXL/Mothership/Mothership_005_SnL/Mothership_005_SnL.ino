// Space'n'Lasers
// Stepper Control Board for Spaceship


// axl@realaxl.de - with
// 2012-12-26 Arduino 1.0.1; AccelStepper 1.39
// 19.01.2016 Arduino 1.6.2; AccelStepper 1.49 (x230)
// 24.01.2016 support for Space'n'Lasers protocol
//    A800 home
//    A801 ping/pong

// based on AccelStepper / Bounce.pde
// http://www.airspayce.com/mikem/arduino/AccelStepper/
//
// -*- mode: C++ -*-
//
// Make a single stepper bounce from one limit to another
//
// Copyright (C) 2012 Mike McCauley
// $Id: Random.pde,v 1.1 2011/01/05 01:51:01 mikem Exp mikem $

// Define a stepper and the pins it will use
// AccelStepper stepper; // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
#include <AccelStepper.h>
AccelStepper stepper(1, 2, 3);

long p = 0;                 // relative position [steps]
long home_pos = 0;          // home position = 0 [steps]
long p_min = 1000;          // far left ping/pong position [steps]
long p_max = 3000;          // far right ping/pongposition [steps]

// normal operation
float n_speed = 400;        // steps / sec
float n_acceleration = 200; // steps / sec / sec

float s_speed = 400;        // steps / sec
float s_acceleration = 800; // steps / sec / sec

// serial command processor
byte inByte = 0;         // incoming serial byte
byte cmd;                // command (1 character)
long val;                // value
boolean val_sig = 1;     // signature

// program finite state machine
byte state = 0;

const int HOMESWITCH = 4;

int receive_magic = 0; // to receive the magical A00x String

void setup()
{
  // setup the stepper object
  stepper_config(n_speed, n_acceleration * 8);
  stepper.moveTo(home_pos + p);

  pinMode(HOMESWITCH, INPUT);
  val_sig = false;

  // start serial port at 9600 bps and wait for port to open:
  Serial.begin(9600);
//  Serial.println(stepper.distanceToGo());
  Serial.flush();
  
  state = 0;
}


void loop() {
  // call this as much as you can ...
  stepper.run();

  // did we hit the home switch?
  if (!digitalRead(HOMESWITCH)) {
    if (true) { // (stepper.targetPosition() < stepper.currentPosition()) {
      stepper_home();
      stepper_config(n_speed, n_acceleration * 8);
      stepper.moveTo(home_pos + 50);
      //stepper.stop();
      state = 1;
    }
  }

  // did we reach the stepper destination?
  if (stepper.distanceToGo() == 0) {
    switch (state) {
      case 0: // init --> move to home (far left)
        stepper_config(n_speed, n_acceleration * 2);
        stepper.moveTo(-300000);
        state ++;
        break;
      case 1: // home reached
        stepper_home();
        stepper_config(n_speed, n_acceleration * 2);
        stepper.moveTo(home_pos + 10);
        state ++;
        write_status_to_serial();
        break;
      case 2: // home reached
        stepper_home();  // new and final home!
        stepper_config(n_speed, n_acceleration);
        state ++;
        write_status_to_serial();
        break;
      case 3:
        p = 0;
        break;
      case 4: // ping / pong
        if (p <= p_min) {
          p = p_max;
        } else {
          p = p_min;
        }
        stepper.moveTo(home_pos + p);
        write_status_to_serial();
        break;
    }
  }


  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();

    switch (receive_magic) {
      case 0:
        receive_magic = (inByte == 'A') ? 1 : 0;
        break;
      case 1:
        receive_magic = (inByte == '8') ? 2 : 0;
        break;
      case 2:
        receive_magic = (inByte == '0') ? 3 : 0;
        break;
      case 3:
        switch (inByte) {
          case '0':
            if (state >= 3) {
              stepper.moveTo(home_pos);
              //Serial.println("force home");
              p = 0;
              state = 0;
            }
            break;
          case '1':
            if (state == 3) {
              state = 4;
            }
            break;
        }
        receive_magic = 0;
        write_status_to_serial();
        break;
    }
  }
}


void stepper_home() {
  home_pos = stepper.currentPosition();
}

void stepper_config(int s, int a) {
  s_speed = s;
  s_acceleration = a;
  stepper.setMaxSpeed(s_speed);
  stepper.setAcceleration(s_acceleration);
}


void write_status_to_serial() {
  /*
  Serial.write('d');
  Serial.write(';');
  Serial.print(state); // was: cmd !!!! 18.01.2016
  Serial.write(';');
  Serial.print(p);
  Serial.write(';');
  Serial.write('H');
  Serial.print(home_pos);
  Serial.write(';');
  Serial.write('s');
  Serial.print(s_speed);
  Serial.write(';');
  Serial.write('a');
  Serial.println(s_acceleration);
  */
}

