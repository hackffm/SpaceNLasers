/* 
 -------------------------------------------------------------------------------
 Starfield background for Space'n'Lasers game
 14.12.2015
 AXL for Hackerspace Frankfurt
 Processing 3.x, Windows 7/10
 -------------------------------------------------------------------------------
 */

// Center of the processing window
float mid_x, mid_y;

// center of projection - Z distance
float z_cop = -1000.0;

// rotation angle and helper vars
float alpha = 0.0;
float sin_alpha = 0, cos_alpha = 0;

// max. radius for star spawn
float r_spawn;

// center of projection "star"
star COP = new star(0.0, 0.0, z_cop);

// final String font_path = "C:/Users/axl/Documents/Seafile/prj/Space'n'Lasers/ressources/fonts/";
final String base_path     = "../../ressources/";
final String font_path     = base_path + "fonts/";
final String config_path   = base_path + "config/";
final String sqlite_path   = base_path + "sqlite/";
final String score_path    = base_path + "scores/";

// -------------------------------------------------------------------------------

void setup() {
  //size(800, 500);
  fullScreen(2);
  colorMode(HSB, 255);
  background(0);
  mid_x = width / 2;
  mid_y = height / 2;
  r_spawn = max(mid_x, mid_y) / 2;

  noStroke();
  fill(255);
  noSmooth();

  int i = 0;
  while (i < star_density) {
    float r = 5 + random(r_spawn);
    float phi = random(PI * 2);
    stars.add(new star(r * cos(phi), r * sin(phi), z_cop + random(400.0 - z_cop)));
    i ++;
  }

  setup_screen();
  generate_SnL_String();
  setup_player();
  setup_JSON();
  background(0);
}


void draw() {
  check_JSON();

  float m = millis();
  noStroke();

  flash_toggle = 1 - flash_toggle;
  if ((flash_on) && (players[flash_toggle].score != last_players[flash_toggle].score)) { 
    last_players[flash_toggle].score = players[flash_toggle].score;
    background(players[flash_toggle].col);
  } else {
    fill(0, 0, 0, 50);
    rect(0, 0, width, height);
  }


  // wobble the rotation angle left & right
  alpha = PI * sin(millis() / 6000.0);

  float dz = 1;//6. + 15.0 * sin(millis()/1000.0);
  for (int i = 0; i < stars.size(); i++) {
    if (stars.get(i).mode == STAR_MODE_ONCE) {
      stars.get(i).z -= dz * 4; // move star
      if (stars.get(i).z < -800) {
        stars.get(i).x +=  random(2) - 1;
        stars.get(i).y +=  random(2) - 1;
      }
    } else {
      stars.get(i).z -= dz; // move star
    }
  }

  int i = 0;  
  while (i < stars.size()) {
    if (stars.get(i).display()) {
      // star out of viewport --> decision live or die?
      switch (stars.get(i).mode) {
      case STAR_MODE_NORMAL:
        float r = 10 + random(r_spawn); // reset stars that have left the field of view
        float phi = random(PI * 2);
        stars.get(i).set(r * cos(phi), r * sin(phi), 100.0 + random(200));
        break;
      case STAR_MODE_ONCE:
        stars.remove(i);
        break;
      }
    }
    i++;
  }
  //println(stars.size() + " stars in " + (millis() - m) + " millis()");


  if (random(333) < 2) {
    add_star_pattern(invader);
  }


  draw_scores();
}