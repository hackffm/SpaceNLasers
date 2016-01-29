// Space'n'Lasers Game Lobby
// 19.01.2016

final String module = "SnL_Lobby";

// final String font_path = "C:/Users/axl/Documents/Seafile/prj/Space'n'Lasers/ressources/fonts/";
final String base_path     = "../../ressources/";
final String font_path     = base_path + "fonts/";
final String config_path   = base_path + "config/";
final String sqlite_path   = base_path + "sqlite/";
final String score_path    = base_path + "scores/";

final int MODE_START = 0;
final int MODE_HIGHSCORES = 1;
final int MODE_SHOW_CURRENT = 2;
final int MODE_SHOW_NEXT = 3;
final int MODE_ENTER_NAME = 4;
final int MODE_FADE = 1000;


int mode = MODE_START;
int mode_timer = 1000;
int mode_after_fade = MODE_START;
int mode_timer_after_fade = 1000;

int last_loop_millis = millis();
int delta_millis = millis();

void setup() {
  setup_fonts();
  read_config_XML("menu_god_config.xml");

  setup_game_modes();

  setup_players();
  
  setup_highscore_entries();
  load_scores(game_modes.get(game_mode));
  
  setup_JSON();
  setup_serial();

  //size (1024, 768);
  fullScreen(2);
  background(0);
}


void draw() {
  delta_millis = millis() - last_loop_millis;

  check_JSON();

  switch (mode) {
  case MODE_START:
    show_Startscreen(128 + mode_timer);
    break;
  case MODE_HIGHSCORES:
    show_HighScores(game_mode);
    break;
  case MODE_SHOW_CURRENT:
    show_Game(0);
    break;
  case MODE_SHOW_NEXT:
    show_Game(1);
    break;
  case MODE_ENTER_NAME:
    show_EnterName();
    break;
  case MODE_FADE:
    show_Fade();
    break;
  }

  if (mode_timer <= 0) { // mode switch
    switch (mode) {
    case MODE_START:
      load_scores(game_modes.get(game_mode)); // ARGH
      switch_mode(MODE_HIGHSCORES, 2000);
      break;
    case MODE_HIGHSCORES:
      // check for new scorees here ?   load_scores(game_mode);
      switch_mode_faded(MODE_SHOW_CURRENT, 2000);
      break;
    case MODE_SHOW_CURRENT:
      switch_mode_faded(MODE_SHOW_NEXT, 2000);
      break;
    case MODE_SHOW_NEXT:
      switch_mode_faded(MODE_START, 1000);
      break;
    case MODE_FADE:
      switch_mode(mode_after_fade, mode_timer_after_fade);
      break;
    }
  }

  if (mode_timer > 0) {
    mode_timer = max(0, mode_timer - delta_millis); // decrease the timer
  }


  last_loop_millis = millis();
}


void switch_mode(int new_mode, int timeout) {
  mode = new_mode;
  mode_timer = timeout;
  // println("Switched to mode " + mode);
}


void switch_mode_faded(int new_mode, int timeout) {
  mode_after_fade = new_mode;
  mode_timer_after_fade = timeout;
  mode = MODE_FADE;
  mode_timer = 1000;
  // println("Switched to mode " + mode + " (faded)");
}


void keyPressed() {
  switch (key) {
  case 'n' :
    switch_mode(MODE_ENTER_NAME, 10000);
    temp_player_name = next_players[temp_player].name;
    break;
  case '1' :
    switch_mode(MODE_ENTER_NAME, 10000);
    temp_player = 0;
    temp_player_name = next_players[temp_player].name;
    break;
  case '2' :
    switch_mode(MODE_ENTER_NAME, 10000);
    temp_player = 1;
    temp_player_name = next_players[temp_player].name;
    break;
  case 's' :
    start_new_game();
    send_JSON(send_gamestart());
    switch_mode(MODE_START, 1000);
    break;
  case 'A' :
    send_JSON(send_abort());
    break;
  case 'b':
    send_JSON(send_gameinfo());
    break;
  case 'g':
    send_JSON(send_gameover());
    break;
  case 'r':
    setup_JSON();
    break;
  case 'm':
    next_game_mode = (next_game_mode + 1) % game_modes.size();
    switch_mode(MODE_SHOW_NEXT, 2000);
    break;
  }

  switch (keyCode) {
  case ENTER :
    if (mode == MODE_ENTER_NAME) {
      next_players[temp_player].name = temp_player_name;
    }
    switch_mode(MODE_SHOW_NEXT, 2000);
    break;
  case ESC :
    switch_mode(MODE_START, 1000);
    key = 0; 
    keyCode = 0;
    break;
  }
}

void mousePressed() {
  if (mode == MODE_ENTER_NAME) {
    if (mouseButton == LEFT) {
      if (temp_player_name.length() < player_name_max) {
        temp_player_name += char(name_chars.get(name_wheel));
      }
    }
    if (mouseButton == RIGHT) {
      if (temp_player_name.length() > 0) {
        temp_player_name = temp_player_name.substring(0, temp_player_name.length() - 1);
      }
    }
  }
}