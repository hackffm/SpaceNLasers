// game mode config

StringList game_modes = new StringList();

int game_mode = 1;
int next_game_mode = 0;

void setup_game_modes() {
  game_modes.append("shootingGallery");
  game_modes.append("domination");
}


void start_new_game() {
  game_mode = next_game_mode;
  // switch names
  for (int i = 0; i < max_players; i ++) {
    players[i].score = 0;
  }
}