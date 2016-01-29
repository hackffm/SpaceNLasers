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


// rotate the f grid content
// h = horizontal, v = vertical
// allways rotates full grid
void rotate_f() {
  boolean tf[][] = new boolean[w_max][h_max]; // temporary buffer
  int tx, ty;

  for (int iy = 0; iy < h_max; iy ++) {
    tx = w_max - 1 - iy;
    for (int ix = 0; ix < w_max; ix ++) {
      ty = ix;
      tf[ix][iy] = f[tx][ty];
    }
  }

  for (int iy = 0; iy < h_max; iy ++) {
    for (int ix = 0; ix < w_max; ix ++) {
      f[ix][iy] = tf[ix][iy];
    }
  }
  int t = w;
  w = w_max;
  h = h_max;
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
