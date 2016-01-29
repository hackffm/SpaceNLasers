// --------------------------------------------------------------------------------
// read machine_config.xml / 2015-05-14
// --------------------------------------------------------------------------------
boolean read_config_XML(String xml_file) {
  XML xml = loadXML(config_path + xml_file);  // centralized config folder

  XML configuration = xml.getChild("serial");
  tty        = configuration.getChild("tty").getContent();
  tty_speed  = int(configuration.getChild("tty_speed").getContent());
  tty_enable = boolean(configuration.getChild("enable").getContent());

  gamemaster_ip     = xml.getChild("gamemaster").getChild("ip").getContent();
  gamemaster_port   = int(xml.getChild("gamemaster").getChild("port").getContent());
  gamemaster_enable = boolean(xml.getChild("gamemaster").getChild("enable").getContent());

  println("read_config_XML()");
  println("tty: (" + tty_enable + ") " + tty + " @ " + tty_speed + " bps");
  println("gamemaster: (" + gamemaster_enable + ") " + gamemaster_ip + ":" + gamemaster_port);

  return(true);
}