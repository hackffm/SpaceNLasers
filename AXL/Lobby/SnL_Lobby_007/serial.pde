import processing.serial.*;
String tty = "x";
int tty_speed = 9600;
boolean tty_enable = false;

String serial_String = "";
Serial serial_Port;  // The serial port

void setup_serial() {
  boolean tty_found = false;

  if (tty_enable) {
    // Open the port you are using at the rate you want:
    for (int i = 0; i < Serial.list().length; i++) {
      if (Serial.list()[i].equals(tty)) {
        println("Port " + tty + " found in Serial.list() at position " + i + ".");
        serial_Port = new Serial(this, tty, tty_speed);
        tty_found = true;
      }
    }
  }

  if (tty_found) {
    serial_Port.clear();
  } else {
    tty_enable = false;
  }
}


void serialEvent(Serial p) {
  serial_String = p.readStringUntil(10);
  if (serial_String != null) {
    println(serial_String);

    int e = 0;

    char a = serial_String.charAt(0);

    if (a == '-') {
      char b = serial_String.charAt(1);
      e = (int) -(b - 48);
    }
    if (a == '+') {
      char b = serial_String.charAt(1);
      e = (int) +(b - 48);
    }

    switch(a) {
      case 'A' :
        switch_mode(MODE_ENTER_NAME, 10000);
        temp_player = 1;
        temp_player_name = next_players[temp_player].name;
        break;
      case 'B' :
        switch_mode(MODE_ENTER_NAME, 10000);
        temp_player = 0;
        temp_player_name = next_players[temp_player].name;
        break;
    }
    if (mode == MODE_ENTER_NAME) {
      switch(a) {
      case 'C' :
        if (temp_player_name.length() > 0) {
          temp_player_name = temp_player_name.substring(0, temp_player_name.length() - 1);
        }
        break;
      case 'E' :
        if (temp_player_name.length() < player_name_max) {
          temp_player_name += char(name_chars.get(name_wheel));
        }
        break;
      }
    }

    name_wheel -= e;
    if (name_wheel < 0) {
      name_wheel = name_num_chars + name_wheel;
    }
    if (name_wheel >=  name_num_chars) {
      name_wheel = name_wheel - name_num_chars;
    }
  }
}