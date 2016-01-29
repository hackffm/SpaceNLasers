void serialEvent(Serial p) { 
  serial_String = p.readStringUntil(10); 

  if (serial_String != null) {
    String[] q = splitTokens(serial_String, ";");
    char cmd = q[1].charAt(0);

    serial_String = trim(serial_String);
    switch (serial_String.charAt(0)) {
      case 'k':
        println("<--    " + serial_String + " / response on " + cmd + " / Queue: " + Q.size() + " / run_level: " + run_level);
        wait_for_k = false;
        break;
      case 'd':
        println("<--    " + serial_String + " (d_received)");
        d_received = true;
        break;
      default:
        println("<--    " + serial_String + " (dump only)");
        break;
    }
  }
}
