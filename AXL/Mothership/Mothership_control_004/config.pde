// --------------------------------------------------------------------------------
// read machine_config.xml / 2015-05-14
// --------------------------------------------------------------------------------
boolean read_config_XML(String xml_file) {
  XML xml = loadXML(config_path + xml_file);  // centralized config folder
  
  XML configuration = xml.getChild("serial");
  tty       = configuration.getChild("tty").getContent();
  tty_speed = int(configuration.getChild("tty_speed").getContent());
  
  println("read_config_XML(): tty from XML: " + tty + " (" + tty_speed + ")");
  
  return(true);
}
