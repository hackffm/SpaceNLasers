import socket
import json

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

DISPLAY_PORT_NUMBER=1339

class Display:
	"""Abstraction of a display for scores and stuff."""
	def __init__(self, targetHostname, players):
		self.targetHostname=targetHostname
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((targetHostname, DISPLAY_PORT_NUMBER))
		self.state={}

		self.send_json({"players":[{"name":p.name,"color":p.color} for p in players]})
	
	def send(self):
		self.send_json(self.state)
	
	def send_json(self,data):
		j=json.dumps(data)+"\0"
		s.send(j)
