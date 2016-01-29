// JSON communication

import processing.net.*;

Client myClient;

String gamemaster_ip = "";
int gamemaster_port = 0;
boolean gamemaster_enable = false;

void setup_JSON() {
  if (gamemaster_enable) {
    myClient = new Client(this, gamemaster_ip, gamemaster_port);
  }
}

void send_JSON(String s) {
  if (gamemaster_enable) {
    myClient.write(s);
  }
}


void check_JSON() {
  if ((gamemaster_enable) && (myClient.available() > 0)) {
    String jsonRow = myClient.readStringUntil(0);
    println("message from: " + myClient.ip() + " : " + jsonRow);

    if ((jsonRow != null) && (trim(jsonRow) != "")) {
      JSONObject json = JSONObject.parse(jsonRow);
      String b = "";
      for (Object a : json.keys()) {
        b = (String) a;
        printredln("Processing JSON: " + b);

        if (b.equals("gameinfo")) {
          JSONObject gameinfo = json.getJSONObject("gameinfo");
          JSONArray j_values = gameinfo.getJSONObject("scores").getJSONObject("score").getJSONArray("values");

          for (int i = 0; i < min(j_values.size(), max_players); i ++) {
            print("scores " + i + " = " + j_values.getInt(i) + " / ");
            players[i].score = j_values.getInt(i);
          }
        }

        if (b.equals("gameover")) {
          for (int i = 0; i < max_players; i ++) {
            println("gameover: adding " + players[i].name + " / " + players[i].score);
            add_score(players[i].name, players[i].score);
          }
          save_scores(game_modes.get(game_mode));
        }
      }
    }
  }
}

String send_gamestart() {
  JSONObject json = new JSONObject();

  JSONObject j_gamestart = new JSONObject();
  JSONObject j_players = new JSONObject();
  JSONArray j_players_a = new JSONArray();

  for (int i = 0; i < players.length; i ++) {
    JSONObject j_player = new JSONObject();
    j_player.setString("name", players[i].name);
    j_player.setString("color", hex(players[i].col, 6));
    j_players_a.setJSONObject(i, j_player);
  }

  j_players.setJSONArray("players", j_players_a);

  JSONObject j_game = new JSONObject();
  j_game.setString("mode", game_modes.get(game_mode));
  j_game.setInt("duration", 0);

  j_players.setJSONObject("game", j_game);

  j_gamestart.setJSONObject("gamestart", j_players);

  j_players.setString("consoleoutput", "STARTING");


  //println(j_gamestart);

  String a = j_gamestart.toString() + char(0);

  println(a.replace("\n", ""));
  println("-------------------------------------------------------------------------------");

  // println(json);
  //saveJSONObject(json, "data/new.json");

  return(a);
}


String send_gameinfo() {
  JSONObject json = new JSONObject();

  JSONObject j_gamestart = new JSONObject();

  // add scores to JSON
  JSONObject j_scores = new JSONObject();
  JSONObject j_score = new JSONObject();
  JSONArray j_scores_a = new JSONArray();

  JSONArray j_values = new JSONArray();
  for (int i = 0; i < players.length; i ++) {
    j_values.setInt(i, players[i].score);
  }

  j_score.setJSONObject("score", new JSONObject().setJSONArray("values", j_values));
  j_scores.setJSONObject("scores", j_score);
  j_gamestart.setString("consoleoutput", "");

  j_gamestart.setJSONObject("gameinfo", j_scores);

  String a = j_gamestart.toString() + char(0);

  println(a);
  println("-------------------------------------------------------------------------------");

  return(a);
}


String send_abort() {
  JSONObject json = new JSONObject();

  json.setJSONObject("abort", new JSONObject());

  String a = json.toString() + char(0);

  println(a);
  println("-------------------------------------------------------------------------------");

  return(a);
}


String send_gameover() {
  JSONObject json = new JSONObject();

  json.setJSONObject("gameover", new JSONObject());

  String a = json.toString() + char(0);

  println(a);
  println("-------------------------------------------------------------------------------");

  return(a);
}