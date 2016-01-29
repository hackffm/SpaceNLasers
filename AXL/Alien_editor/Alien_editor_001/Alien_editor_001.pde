final int w_max = 40;
final int h_max = 40;

int h = 10, w = 10;

boolean f[][] = new boolean[w_max][h_max];

float grid_w, grid_h;

boolean paint = true;
boolean mirror = false;

void setup() {
  size (500, 500);

  draw_grid();
}

void draw() {
}

// -------------------------------------------------------------------------------
// Mouse
// -------------------------------------------------------------------------------

void mouseDragged() {
   set_pixel(mouseX, mouseY);
}

void mousePressed() {
   set_pixel(mouseX, mouseY);
}

void set_pixel(int mx, int my) {
  int fx = int((float)mx / grid_w);
  int fy = int(((float)my - 20) / grid_h);
  
  if ((fx >= 0) && (fx < w) && (fy >= 0) && (fy < h)) {
    f[fx][fy] = paint;
    draw_pixel(fx, fy);
  
    if (mirror) {
      int mirror_x = w - 1 - fx;
      f[mirror_x][fy] = paint;
      draw_pixel(mirror_x, fy);
    }
  }
}

// -------------------------------------------------------------------------------
// Keyboard
// -------------------------------------------------------------------------------

void keyPressed() {
  switch (key) {
    case 'a' :
      w = w_max;
      h = h_max;
      break;
    case 'w' :
      w = min(w + 1, w_max);
      break;
    case 'W' :
      w = max(w - 1, 2);
      break;
    case 'h' :
      h = min(h + 1, h_max);
      break;
    case 'H' :
      h = max(h - 1, 2);
      break;
    case ' ' :
      paint = !paint;
      break;
    case 'm' :
      mirror = !mirror;
      break;
    case 'f' :
      flip_f('h');
      break;
    case 'F' :
      flip_f('v');
      break;
    case 'c' :
      crop_f();
      break;
    case 'i' :
      invert_f();
      break;
  }


  switch (keyCode ) {
    case UP :
      move_f(0, 1);
      break;
    case DOWN :
      move_f(0, -1);
      break;
    case LEFT :
      move_f(1, 0);
      break;
    case RIGHT :
      move_f(-1, 0);
      break;
    case DELETE :
      fill_f(false);
      break;
  }
  draw_grid();
}





// -------------------------------------------------------------------------------
// Screen stuff
// -------------------------------------------------------------------------------

void draw_grid() {
  background(128);
  draw_info();
  
  stroke(0);
  
  grid_w = (float) width / w;
  grid_h = (float) (height - 20) / h;
  
  grid_w = min(grid_w, grid_h);
  grid_h = grid_w;
  
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      draw_pixel(ix, iy);
    }
  }
}

void draw_pixel(int x, int y) {
  float fx = grid_w * x;
  float fy = grid_h * y + 20;
  
  fill((f[x][y]) ? 255 : 64);
  rect(fx, fy, grid_w, grid_h);
}

void draw_info() {
  fill(255);
  stroke(255);
  
  text ("Paint: " + paint + " / Mirror: " + mirror, 10, 16);
  text ("Width: " + int(w) + " / Height: " + int(h), width / 2, 16);
}


// -------------------------------------------------------------------------------
// image manipulation
// -------------------------------------------------------------------------------

void fill_f(boolean mode) {
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      f[ix][iy] = mode;
    }
  }
}

void invert_f() {
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      f[ix][iy] = !f[ix][iy];
    }
  }
}

// move the f grid content
// in w/h by deltas dx, dy (typically -1, 0 or +1)
// and copy back to f
// limited to visible range w/h
void move_f(int dx, int dy) {
  boolean tf[][] = new boolean[w][h]; // temporary buffer
  int tx, ty;
  
  for (int iy = 0; iy < h; iy ++) {
    ty = iy + dy;
    if (ty < 0)  { ty = h + ty; }
    if (ty >= h) { ty = ty - h; }
    for (int ix = 0; ix < w; ix ++) {
      tx = ix + dx;
      if (tx < 0)  { tx = w + tx; }
      if (tx >= w) { tx = tx - w; }
      tf[ix][iy] = f[tx][ty];
    }
  }

  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      f[ix][iy] = tf[ix][iy];
    }
  }
}


// flip the f grid content
// h = horizontal, v = vertical
// limited to visible range w/h
void flip_f(char mode) {
  boolean tf[][] = new boolean[w][h]; // temporary buffer
  int tx, ty;

  for (int iy = 0; iy < h; iy ++) {
    ty = (mode == 'v') ? h - 1 - iy : iy;
    for (int ix = 0; ix < w; ix ++) {
      tx = (mode == 'h') ? w - 1 - ix : ix;
      tf[ix][iy] = f[tx][ty];
    }
  }

  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      f[ix][iy] = tf[ix][iy];
    }
  }
}  


// flip the f grid content
// h = horizontal, v = vertical
void crop_f() {
  boolean tf[][] = new boolean[w][h]; // temporary buffer
  int x_min = w - 1, x_max = h - 1, y_min = 0, y_max = 0;
  boolean copy_on = false;
  
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      if (f[ix][iy]) {
        if (!copy_on) {
          x_min = ix;
          y_min = iy;
          x_max = ix;
          y_max = iy;
          copy_on = true;
        } else {
          x_min = min(x_min, ix);
          y_min = min(y_min, iy);
          x_max = max(x_max, ix);
          y_max = max(y_max, iy);
        }
      }
    }
  }
  
  for (int iy = y_min; iy <= y_max; iy ++) {
    for (int ix = x_min; ix <= x_max; ix ++) {
      tf[ix - x_min][iy - y_min] = f[ix][iy];
    }
  }

  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      f[ix][iy] = tf[ix][iy];
    }
  }
  
  w = max(2, 1 + x_max - x_min);
  h = max(2, 1 + y_max - y_min);
}  

