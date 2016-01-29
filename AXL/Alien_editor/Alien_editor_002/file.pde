void write_data_file() {
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      if(f[ix][iy]) {
        print ("1,");
      } else {
        print ("0,");
      }
    }
    println();
  }
}
