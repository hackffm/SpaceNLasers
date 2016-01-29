
// grid definition
final int w_max = 40;
final int h_max = 40;

int h = 10, w = 10;

boolean f[][] = new boolean[w_max][h_max];

float grid_w, grid_h;

// modes
boolean paint = true;
boolean mirror = false;

// screen defintion
final int info_line_height = 20;

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
  int fy = int(((float)my - info_line_height) / grid_h);
  
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


void set_hline(int mx, int my) {
  int fx = int((float)mx / grid_w);
  int fy = int(((float)my - info_line_height) / grid_h);
  
  if ((fx >= 0) && (fx < w) && (fy >= 0) && (fy < h)) {
    int mem_fx = fx;
    f[fx][fy] = paint;
    draw_pixel(fx, fy);
    fx --;
    while((fx >= 0) && (f[fx][fy] != paint)) {
      f[fx][fy] = paint;
      draw_pixel(fx, fy);
      fx --;
    }
    fx = mem_fx + 1;
    while((fx < w) && (f[fx][fy] != paint)) {
      f[fx][fy] = paint;
      draw_pixel(fx, fy);
      fx ++;
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
    case 'r' :
      rotate_f();
      crop_f();
      break;
    case 'c' :
      crop_f();
      break;
    case 'i' :
      invert_f();
      break;
    case 'l' :
      set_hline(mouseX, mouseY);
      break;
    case 'o' :
      write_data_file();
      break;  
    case 'b' :
      add_border_to_f();
      break;  
    }


  switch (keyCode) {
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