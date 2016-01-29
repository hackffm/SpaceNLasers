import processing.net.*;

Server myServer;

int last_JSON_timestamp = 0;

void setup_JSON() {
  myServer = new Server(this, 5000);
}

void check_JSON() {
  Client thisClient = myServer.available();

  if (thisClient != null) {
    if (thisClient.available() > 0) {
      String jsonRow = thisClient.readStringUntil(0);
      last_JSON_timestamp = millis();
      println("message from: " + thisClient.ip() + " : " + jsonRow);

      if ((jsonRow != null) && (trim(jsonRow) != "")) {
        process_JSON(jsonRow);
      }
    }
  }
}


void process_JSON(String jsonRow) {
  JSONObject json = JSONObject.parse(jsonRow);
  //println(json);
  //println(json.keys());

  String b = "";
  for (Object a : json.keys()) {
    b = (String) a;
    printredln("Processing JSON: " + b);

    if (b.equals("capabilities")) {
      //thisClient.write(send_JSON_gamestart());
      // println("Send gamestart - DONE");
    }

    if (b.equals("gamestart")) {
      JSONObject gamestart = json.getJSONObject("gamestart");

      game_mode = gamestart.getJSONObject("game").getString("mode");
      if (game_mode.equals("shootingGallery")) {
        flash_on = true;
      } else {
        flash_on = false;
      }
      printredln("game_mode: " + game_mode + " / flash_on = " + flash_on);
      
      JSONArray j_players = gamestart.getJSONArray("players");
      println("gamestart received");
      for (int i = 0; i < min(j_players.size(), max_players); i ++) {
        JSONObject j_player = j_players.getJSONObject(i);
        players[i].name = j_player.getString("name");
        players[i].col = color(unhex(j_player.getString("color")) + 255 * unhex("1000000"));
        println("color " + i + " = " + hex(players[i].col));
      }
      console = gamestart.getString("consoleoutput");
      console = trim(console);
      if (!console.equals("")) {
        console_timeout = millis() + 4000;
        print("console: " + console + " / ");
      }
    }

    if (b.equals("gameinfo")) {
      JSONObject gameinfo = json.getJSONObject("gameinfo");
      JSONArray j_values = gameinfo.getJSONObject("scores").getJSONObject("score").getJSONArray("values");


      for (int i = 0; i < min(j_values.size(), max_players); i ++) {
        print("scores " + i + " = " + j_values.getInt(i) + " / ");
        players[i].score = j_values.getInt(i);
      }

      // console string
      console = gameinfo.getString("consoleoutput");
      console = trim(console);
      if (!console.equals("")) {
        console_timeout = millis() + 4000;
        print("console: " + console + " / ");
      }
      //draw_scores();
    }

    if (b.equals("consoleoutput")) {
      if (!console.equals("")) {
        console_timeout = millis() + 4000;
        print("console: " + console + " / ");
      }
    }
  }

  if (b.equals("gameover")) {
    // process game over, scores, new names
    console = "GAME OVER";
    console_timeout = millis() + 20000;
  }

  println();
  println("-------------------------------------------------------------------------------");

  //jsonFromGameMaster = new JSONObject(jsonRow);
}