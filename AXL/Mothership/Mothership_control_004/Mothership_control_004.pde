/*

Space'n'Lasers
Mothership_control_001

03.01.2016 by AXL for Hackerspace FFM

002 - 2016-01-03 - sync mode, Q working, low level commands working
003 - 2016-01-03 - simple home command sequence 

*/


// --------------------------------------------------------------
// low level machine state
// --------------------------------------------------------------

int run_level = -1;
int init_attempt = 0;
int m = millis();

// low level job queue - will be transferred to serial port
StringList Q;

// wait for Arduino to send k (OK response)
boolean wait_for_k = false;

import processing.serial.*;
String tty = "x";
int tty_speed = 9600;

final char lf = char(10);    // Linefeed in ASCII
String serial_String = "";
Serial serial_Port;  // The serial port

// statistics
int total_commands_send = 0;


// --------------------------------------------------------------
// crappy machine control test
// --------------------------------------------------------------
int home = 0;
boolean d_received = false;

// --------------------------------------------------------------
// Paths
// --------------------------------------------------------------
final String image_path  = "../data/images/";
final String config_path = "../data/config/";
final String output_path = "../data/rendering_output/";
final String font_path   = "../data/fonts/";


void setup() {
  size(640, 640);
  background(64);


  // initialize the job queue
  Q = new StringList();
  
  // List all the available serial ports
  println("Serial.list()");
  println(Serial.list());
  println("-------------------------------------------------------------------------------");

  
  read_config_XML("mothership_config.xml");
  
  
  boolean tty_found = false;
  // Open the port you are using at the rate you want:
  for (int i = 0; i < Serial.list().length; i++) {
    if (Serial.list()[i].equals(tty)) {
      println("Port " + tty + " found in Serial.list() at position " + i + ".");
      serial_Port = new Serial(this, tty, tty_speed);
      tty_found = true;
    }
  }

  if (tty_found) {
    serial_Port.clear();
    append_to_Q("i;s 1200;a 4000;h;H;m0");
    wait_for_k = true;
    run_level = 0;
  }  
  
  
  // initialize the loop timestamp
  m = millis();
  println("-------------------------------------------------------------------------------");
}



void draw() {
  if (run_level == 0) {
    if (!wait_for_k) {
      run_level ++;
      Q.remove(0);
      println("run_level: " + run_level);
    } else {
      // resend on timeout    
      if ((millis() - m) > 500) {
        serial_Port.write(Q.get(0));
        serial_Port.write(10);
        m = millis();

        init_attempt ++;
        println("read attempt ... " + init_attempt + " run_level: " + run_level + " (command: " + Q.get(0) + ")");
      }
    }
  } else { 
    // run_level > 0
    if (!wait_for_k) {
      if (Q.size() == 0) {
      }


      if (Q.size() > 0) {
        System.err.println("--> " + Q.get(0));
        serial_Port.write(Q.get(0));
        serial_Port.write(10);
        wait_for_k = true;

        total_commands_send ++;
        Q.remove(0);
      }
    }

    if (d_received) {
      home ++;
      println("*** Next home state = " + home);
      println("-------------------------------------------------------------------------------");
      
      switch (home) {
        case 1:
          append_to_Q("i;s200;a5000;h;H;m-20000");
          break;
        case 2:
          append_to_Q("H;s300;a900;m100");
          break;
        case 3:
          append_to_Q("s160;a2000;m-20000");
          break;
        case 4:
          append_to_Q("H;s300;a133;m100");
          break;
        case 5:
          append_to_Q("H;i;m100");
          break;
        default:
          int pos = int(random(4000));
          int wait = 100 + int(random(2000));
          append_to_Q("w" + wait + ";m" + pos);
          break;
      }
      d_received = false;
    }

//    render_state_stack();
  }
}


// append a ';' separated list of commands to the Queue
void append_to_Q(String s) { 
  String[] q = splitTokens(s, ";");
  
  for (int i = 0; i < q.length; i ++) {
    Q.append(trim(q[i]));
  }
}
