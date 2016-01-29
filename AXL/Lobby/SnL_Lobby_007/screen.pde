// screen

PFont VT323_64, VT323_128, VT323_256;

int name_wheel = 0;
int name_num_chars = 26;

void setup_fonts() {
  VT323_256 = createFont(font_path + "VT323-Regular.ttf", 256);
  VT323_128 = createFont(font_path + "VT323-Regular.ttf", 128);
  VT323_64  = createFont(font_path + "VT323-Regular.ttf", 64);
}  

void show_Startscreen(int y) {
  background(0);

  noStroke();
  textAlign(CENTER);

  textFont(VT323_128);
  fill(#00ffdd);
  text ("Space'n'Lasers", width / 2, y);
}



void show_EnterName () {
  // show_Startscreen(128);
  background(0);
  color blink_color = color(255, 128 + 127 * sin(millis()/100.), 0);

  noStroke();
  textAlign(CENTER);
  textFont(VT323_64);
  fill(#cccccc);
  text ("Enter your name", width / 2, height / 2 - 64);

  textFont(VT323_256);
  //  fill(blink_color);
  fill(players[temp_player].col);
  text (temp_player_name, width / 2, height / 2 + 128);


  //  float rx = min((width - 320) / 2, 400);
  float ry = (height - 128) / 2;
  float rx = min((width - 320) / 2, ry + 160);
  float mx = width / 2;
  float my = (height - 128) / 2 + 96;


  textFont(VT323_128);

  name_num_chars = name_chars.size();
  for (int i = 0; i < name_num_chars; i ++) {
    float a = (float) i / name_num_chars * (2 * PI) + PI / 20 *sin(millis() / 1000.);
    float x = mx + rx * sin(a);
    float y = my - ry * cos(a);
    if (i == name_wheel) { 
      fill(blink_color);
      textFont(VT323_128);
    } else {
      fill(#cccccc);
      textFont(VT323_64);
    }
    text(char(name_chars.get(i)), x, y);
  }
}


void show_Game(int g) {
  show_Startscreen(128);

  player p[] = new player[2]; // p0, p1; // = new player, p1 = new player;
  String title, g_mode;

  textFont(VT323_64);
  fill(#cccccc);
  switch (g) {
  case 0:
    title = "Now playing:";
    p[0] = players[0];
    p[1] = players[1];
    g_mode = game_modes.get(game_mode);
    break;
  default:
    title = "Next match:";
    p[0] = next_players[0];
    p[1] = next_players[1];
    g_mode = game_modes.get(next_game_mode);
    break;
  }

  center_64(title, 1);

  center_64("vs.", 4);

  center_64("Game mode", 8);
  fill(#ffff00);
  center_64(g_mode, 9);

  textFont(VT323_128);

  for (int i = 0; i < 2; i ++) {
    fill(p[i].col);
    if (p[i].score == 0) {
      center_64(p[i].name, 3 + i * 3);
    } else {
      show_HighScore_line(p[i], 3 + i * 3);
    }
  }
}


void show_HighScores(int game_mode) {
  show_Startscreen(128);

  textFont(VT323_64);
  fill(#ffff00);
  fill(#cccccc);
  center_64("Highscores", 1);
  fill(#ffff00);
  center_64(game_modes.get(game_mode), 2);

  fill(#cccccc);
  for (int i = 0; i < highscore_entries; i ++) {
    show_HighScore_line(highscore_entry[i], 4 + i);
  }
}


void show_HighScore_line(player p, int y) {
  int line_len = min((width - 128) / 32, 18);

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


void show_Fade() {
  fill(#000000);
  for (int i = 0; i < 20; i ++) {
    float y = 160 + random(height - 160);
    rect(0, y, width, 4);
  }
}


void center_64(String s, int y) {
  text (s, width / 2, pos_y_64(y));
}

float pos_y_64(int y) {
  return(200 + y * 64);
}



void mouseWheel(MouseEvent event) {
  float e = event.getCount();
  // println(e);

  name_wheel += e;
  if (name_wheel < 0) {
    name_wheel = name_num_chars + name_wheel;
  }
  if (name_wheel >=  name_num_chars) {
    name_wheel = name_wheel - name_num_chars;
  }
}



void printredln (String ln) {
  System.err.println(ln);
}