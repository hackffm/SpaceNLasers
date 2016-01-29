// attributes for the players
final int max_players = 2;
player players[] = new player[max_players];
player last_players[] = new player[max_players];

class player {
  int score;
  String name;
  color col;

  player(String t_name, color t_col) {
    name = t_name;
    col = t_col;
    score = 0;
  }

  void init(String t_name, color t_col) {
    name = t_name;
    col = t_col;
    score = 0;
  }
}

void setup_player() {
  players[0] = new player("UNKNOWN1", #ff0000);
  players[1] = new player("UNKNOWN2", #0000ff);

  last_players[0] = new player("UNKNOWN1", #ff0000);
  last_players[1] = new player("UNKNOWN1", #ff0000);
}

void init_player_for_game() {
  last_players[0] = players[0];
  last_players[1] = players[1];
}