// output functions
// to file?

void write_data_file_01() {
  println();
  println("// Dimensions: " + w + " x " + h + " pixels");
  for (int iy = 0; iy < h; iy ++) {
    for (int ix = 0; ix < w; ix ++) {
      if (f[ix][iy]) {
        print ("1,");
      } else {
        print ("0,");
      }
    }
    println();
  }
  println();
}


void write_data_file_String() {
  println();
  println("// Dimensions: " + w + " x " + h + " pixels");
  for (int iy = 0; iy < h; iy ++) {
    print ("\"");
    for (int ix = 0; ix < w; ix ++) {
      if (f[ix][iy]) {
        print ("#");
      } else {
        print (" ");
      }
    }
    println(".\" +");
  }
  println();
}

// timestamp String, format 2016-01-19_16-30-25
String timestamp() {
  String s = nf(year(), 4) + "-" + nf(month(), 2) + "-" + nf(day(), 2);
  s += "_" + nf(hour(), 2) + "-" + nf(minute(), 2) + "-" + nf(second(), 2);
  return s;
}