// My God, it's full of stars ...
ArrayList<star> stars = new ArrayList<star>();
final int star_density = 333;

final int STAR_MODE_NORMAL = 0;
final int STAR_MODE_ONCE = 1;


class star {
  int id;
  float x, y, z;
  int mode;
  int hue, sat;

  star(float tx, float ty, float tz) {
    x = tx;
    y = ty;
    z = tz;
    mode = STAR_MODE_NORMAL;
    hue = 0; 
    sat = 0;
  }

  void set(float tx, float ty, float tz) {
    x = tx;
    y = ty;
    z = tz;
  }

  // set star mode
  void set_mode(int tmode) {
    mode = tmode;
  }

  // set hue and saturation in HSV color mode
  void set_color(int t_hue, int t_sat) {
    hue = t_hue;
    sat = t_sat;
  }

  boolean display() {
    float f = min(1, (z + 0) / z_cop);
    stroke(hue, sat, f * 255.0);
    fill(hue, sat, f * 255.0);
    float sx = x - COP.z * ((x - COP.x) / (z - COP.z));
    float ty = y - COP.z * ((y - COP.y) / (z - COP.z));

    float a;
    if (mode == STAR_MODE_ONCE) {
      a = alpha * f / 2; //PI + f;//PI * 3.0 * f;
    } else {
      a = alpha * f;
    }
    // a = 0;
    sin_alpha = sin(a);
    cos_alpha = cos(a);

    float sy = sx *  cos_alpha + ty * sin_alpha;
    sx       = sx * -sin_alpha + ty * cos_alpha;

    sx = mid_x + sx;
    sy = mid_y - sy;

    rect(sx, sy, 3*f, 3*f);

    if ((sx < 0) | (sx > width) | (sy < 0) | (sy > height) | (z < z_cop))
      return(true);
    else
      return(false);
  }
}

// -------------------------------------------------------------------------------

String invader = "" +
  "  #     #  ." + 
  "   #   #   ." + 
  "  #######  ." + 
  " ## ### ## ." + 
  "###########." + 
  "# ####### #." + 
  "# #     # #." + 
  "   ## ##   ";

String drelbs = "" +
  "##  ##  ##  ##." +
  "  ##########  ." +
  "##############." +
  "##    ##    ##." +
  "####  ##  ####." +
  "  ##########  ." +
  "  ####  ####  ." +
  "  ####  ####  ." +
  "##############." +
  "##  ##  ##  ##." +
  "####      ####." +
  "  ##  ##  ##  ." +
  "  ##########  ." +
  "    ######    .";


void add_star_pattern(String pattern) {
  float ix = 0, iy = 0;
  int i = 0, j = 0;
  int inv_color = int(random(256));

  float r = 1 + random(r_spawn / 2); // set the shape origin
  float phi = random(PI * 2);
  float chi = random(PI * 2); // shape rotation angle

  float sin_chi = sin(chi);
  float cos_chi = cos(chi);

  float mx = r * cos(phi);
  float my = r * sin(phi);

  while (i < pattern.length()) {  
    switch (pattern.charAt(i)) {
    case '#' :

      float sx = ix *  cos_chi + iy * sin_chi;
      float sy = ix * -sin_chi + iy * cos_chi;

      stars.add(new star((float) mx + sx, (float) my + sy, 100. + ix));
      j = stars.size() - 1;
      stars.get(j).set_color(inv_color, 255);
      stars.get(j).set_mode(STAR_MODE_ONCE);
      break;
    case '.' :
      ix = -1;
      iy ++;
      break;
    }
    ix ++;
    i ++;
  }
}

String SnL = " ";

void generate_SnL_String() {
  text("Space'n'Lasers", 0, 10);
  //text("SPACE'n'LASERS", 0, 10);

  int ix = 0, iy = 0, i = 0;
  while (iy < 13) {
    if (get(ix, iy) != -16777216) {
      SnL += '#';
    } else {
      SnL += ' ';
    }
    ix ++;
    if (ix > 100) {
      ix = 0;
      iy ++;
      SnL += '.';
    }
    i ++;
  }
}  