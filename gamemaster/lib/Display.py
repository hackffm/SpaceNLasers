import socket
import json
import Player

# init
"""
"players": [
	{"name":"Player1","color":"00FF00"},
	{"name":"Player2","color":"FF0000"}
]
"""

# continuous
"""
"values":{
	"scores": {"type":"int",values:[200,182]},
	"area": {"type":"bar",values:[0.3,0.25]}
}
"""

DISPLAY_PORT_NUMBER=5000

class Display:
	"""Abstraction of a display for scores and stuff."""
	def __init__(self, targetHostname, players):
		self.targetHostname=targetHostname
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((targetHostname, DISPLAY_PORT_NUMBER))
		self.state={}

		self.send_json({"players":[{"name":p.name,"color":p.color} for p in players]})
	
	def send(self):
		self.send_json({"values":self.state})
	
	def send_json(self,data):
		j=json.dumps(data)+"\0"
		self.s.send(j)

if __name__=="__main__":
	d=Display("10.0.0.102",[Player.Player("hephaisto","00FF00")])
	d.state["scores"]={"type":"int","values":[100]}
	d.send()
