import socket
import json
import Player

# menugod connects to gamemaster
# g->m capabilities
# gamemaster goes to lobby mode
# m->g gamestart: playernames, colors, gamemode, duration
# game starts
# g->m (continuous) gameinfo: scores, consoleoutput
# m->g (optional) abort: -
# g->m gameover: -
# gamemaster goes to lobby mode

# capabilities
"""
"capabilities": {
	"gamemodes":["domination"]
}
"""

# gamestart
"""
"gamestart": {
	"players": [
		{"name":"Player1","color":"00FF00"},
		{"name":"Player2","color":"FF0000"}
	],
	"game": {"mode":"domination","duration":60}
}
"""

# gameinfo
"""
"gameinfo":{
	"scores":{
		"score": {"type":"int",values:[200,182]},
		"area": {"type":"bar",values:[0.3,0.25]}
	},
	"consoleoutput":{"blablabla"}
}
"""

# abort (any m->g communication aborts!)
"""
"abort":0
"""

# gameover
"""
"gameover":0
"""

DISPLAY_PORT_NUMBER=5000

## Abstraction of a display for scores and stuff.
class MenuGod:
	## Initialises state and sends player information to display.
	def __init__(self, targetHostname, players):
		self.targetHostname=targetHostname
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if targetHostname is None: # server mode
			print("server mode: waiting for connection...")
			self.s.bind("127.0.0.1",DISPLAY_PORT_NUMBER)
			self.s.listen(1)
			conn, addr = s.accept()
			print("connection from {}".format(addr))
			self.connection=conn
		else:
			print("connecting to {}...".format(targetHostname))
			self.s.connect((targetHostname, DISPLAY_PORT_NUMBER))
			print("connected")
			self.connection=self.s

		self.state={}

		self.send_json({"players":[{"name":p.name,"color":p.color} for p in players]})
	
	## Send current state to display.
	def send(self):
		self.send_json({"values":self.state})
	
	def GameOver(self):

	
	## Internal helper function
	def send_json(self,data):
		j=json.dumps(data)+"\0"
		self.connection.send(j)

if __name__=="__main__":
	import time
	d=MenuGod("10.0.0.158",[Player.Player("hephaisto","00FF00")])
	for i in range(10):
		d.state["scores"]={"type":"int","values":[10*i]}
		d.send()
		time.sleep(1.0)
