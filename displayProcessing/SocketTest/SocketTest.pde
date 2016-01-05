import processing.net.*;

Server myServer;
int val = 0;

void setup() {
	// Starts a myServer on port 5204
	myServer = new Server(this, 5000); 
}

void draw() {
	Client thisClient = myServer.available();
	if (thisClient != null) {
		if (thisClient.available() > 0) {
			String jsonRow = thisClient.readString();
			print("mesage from: " + thisClient.ip() + " : " + jsonRow);
			jsonFromGameMaster = new JSONObject(jsonRow);

		}
	}
}