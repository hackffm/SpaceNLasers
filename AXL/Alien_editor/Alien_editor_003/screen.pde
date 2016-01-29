// -------------------------------------------------------------------------------
// Screen stuff
// -------------------------------------------------------------------------------

void draw_grid() {
  background(128);
  draw_info();
  
  stroke(0);
  
  grid_w = (float) width / w;
  grid_h = (float) (height - info_line_height) / h;
  
  grid_w = min(grid_w, grid_h);
  grid_h = grid_w;
  
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      draw_pixel(ix, iy);
    }
  }
  
  if (mirror) {
    stroke(#ff0000);
    float mirror_x = grid_w * (float) w / 2.0;
    rect(mirror_x, info_line_height - 1, 1, 1);
  }
  stroke(0);
}

void draw_pixel(int x, int y) {
  float fx = grid_w * x;
  float fy = grid_h * y + info_line_height;
  
  fill((f[x][y]) ? 255 : 64);
  rect(fx, fy, grid_w, grid_h);
}

void draw_info() {
  fill(255);
  stroke(255);
  
  text ("Paint: " + paint + " / Mirror: " + mirror, 10, 16);
  text ("Width: " + int(w) + " / Height: " + int(h), width / 2 + 10, 16);
}