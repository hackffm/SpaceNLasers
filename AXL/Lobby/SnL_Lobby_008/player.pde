// attributes for the players
final int max_players = 2;
player players[] = new player[max_players]; // players for current match
player next_players[] = new player[max_players]; // players for next match
String player_description[] = new String[max_players]; // description for registration

// Highscore table
final int highscore_entries = 7;
final int player_name_max = 10; // max. lenght in characters
player[] highscore_entry = new player[highscore_entries];


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


void setup_players() {
  players[0] = new player("BLASTER", #ff7700);
  players[1] = new player("BEATME",  #39ff14);

  next_players[0] = new player("", players[0].col);
  next_players[1] = new player("", players[1].col);

  player_description[0] = "ORANGE PLAYER";
  player_description[1] = "GREEN PLAYER";

  setup_name_chars();
}


void setup_highscore_entries() {
  for (int i = 0; i < highscore_entries; i ++) {
    highscore_entry[i] = new player("UNKNOWN", 0);
  }
}


// temp player name
String temp_player_name = "";
int temp_player = 0;

// characters for the "enter name" wheel
IntList name_chars = new IntList();

void setup_name_chars() {
  for (int i = 0; i < 26; i ++) {
    name_chars.append(65 + i);
  }
  
  name_chars.append((int) '_');
  name_chars.append((int) '.');
  name_chars.append((int) '0');

  for (int i = 9; i >= 1; i --) {
    name_chars.append(48 + i);
  }
}