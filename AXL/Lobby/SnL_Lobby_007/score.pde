String[] scores = new String[0];

// load score String file and fill highscore_entry[]
void load_scores(String filename) {
  String score_file = score_path + filename + ".txt";

  scores = loadStrings(score_file);
  scores = sort(scores);
  scores = reverse(scores);
  
  // printredln("load_scores(): " + score_file + " with entries: " + scores.length);

  for (int i = 0; i < highscore_entries; i ++) {
    highscore_entry[i] = get_player_score(i);
  }
}


// save scores[] to a String file
void save_scores(String filename) {
  String score_file = score_path + filename + ".txt";
  saveStrings(score_file, scores);
}


// add an array element to score[]
void add_score(String name, int score) {
  String s = nf(score, 10) + "|" + name;
  //println(s);
  scores = append(scores, s);
  scores = sort(scores);
  scores = reverse(scores);
}


// extract name and score for the concatenated String scores[i]
player get_player_score(int i) {
  player p = new player("UNKNOWN", #000000);
  if (i < scores.length) {
    String[] list = split(scores[i], '|');
    p.name = list[1];
    p.score = int(list[0]);
    //println(list[1]);
  }
  return(p);
}