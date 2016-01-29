// screen

PFont VT323_64, VT323_128, VT323_256;

String console = "SnL BEAMER";
int console_timeout = millis() + 3000;

// screen flashes for each hit?
boolean flash_on = false;
int flash_toggle = 1;


void setup_screen() {
  VT323_256 = createFont(font_path + "VT323-Regular.ttf", 256);
  VT323_128 = createFont(font_path + "VT323-Regular.ttf", 128);
  VT323_64  = createFont(font_path + "VT323-Regular.ttf", 64);
}

void draw_scores() {
  if ((millis() - last_JSON_timestamp) < 2000) {
    textFont(VT323_64);
    textAlign(CENTER);
    for (int i = 0; i < max_players; i ++) {
      fill(players[i].col);
      text(players[i].name + ": "+ players[i].score, (1 + 3 * i) * (width / 5), 40);
    }
    fill(#999900);
    text(game_mode, width / 2, height - 64);
  } else {
    if (random(120) < 2) {
      if (stars.size() < 1000) {
        add_star_pattern(SnL);
      }
    }
  }


  if ((console_timeout - millis()) > 0) {
    noStroke();
    textAlign(CENTER);

    int y0 = height / 2 - 144; // baseline
    int x0 = width / 2;
    textFont(VT323_256);
    float t = sin(millis() / 100.);
    fill(155. + 100. * t);
    text (console, x0, y0);

    textFont(VT323_128);
    for (int i = 0; i < max_players; i ++) {
      fill(players[i].col);
      //text(players[i].name + ": "+ players[i].score, x0, y0 + (i + 2) * 128);
      show_HighScore_line(players[i], 3 + i * 2);
    }
  }
}  



void show_HighScore_line(player p, int y) {
  int line_len = min((width - 128) / 64, 24);
  
  String n = p.name + "";  
  String s = "" + nf(p.score, 1);
  String f = "";
  
  int i = line_len - n.length() - s.length();
  while (i > 0) {
    f = f + ".";
    i --;
  }
 
  center_64(n + f + s, y);
}


void center_64(String s, int y) {
  text (s, width / 2, pos_y_64(y));
}


float pos_y_64(int y) {
  return(200 + y * 64);
}


void printredln (String ln) {
  System.err.println(ln);
}