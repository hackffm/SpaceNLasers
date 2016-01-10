import socket
import json
import Player
import gamemodes

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
		"score": {"type":"int","values":[200,182]},
		"area": {"type":"bar","values":[0.3,0.25]}
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

# protocol or state machine error
"""
"error":"error text"
"""

DISPLAY_PORT_NUMBER=5000

## Exception which is thrown if fully received message is available during game (all message transmissions mean "abort")
class AbortGameException(Exception):
	pass

class FakeMenuGod:
	def __init__(self):
		pass
	def CheckNewGameStart(self):
		return {"players": [{"name":"Player1","color":"00FF00"}],"game": {"mode":"dummy","duration":60}}
	def SendGameInfo(self, info):
		#print("game info: {}".format(info))
		pass
	def GameOver(self):
		print("GAME OVER")


## Abstraction of a display for scores and stuff.
# Usage
# \code
#	m=MenuGod("")
#	# in lobby mode now
#	while(True):
#		gamestart=m.CheckNewGameStart()
#		if gamestart is not None:
#			# use gamestart info to initialize game
#			break
#	
# \endcode
# During game
# \code
#	try:
#		while(True):
#			# game loop
#			m.SendGameInfo(info)
#		m.GameOver()
#	except AbortGameException:
#		# cleanup game
#		return
# \endcode
class MenuGod:
	## Initialises state and sends player information to display.
	# \param targetHostname IP of server to connect to. Use None to use server-mode
	def __init__(self, targetHostname):
		self.state="init"

		self.buffer=""

		# init network
		self.targetHostname=targetHostname
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if targetHostname is None: # server mode
			print("server mode: waiting for connection...")
			self.s.bind(("",DISPLAY_PORT_NUMBER))
			self.s.listen(1)
			conn, addr = self.s.accept()
			print("connection from {}".format(addr))
			self.connection=conn
		else:
			print("connecting to {}...".format(targetHostname))
			self.s.connect((targetHostname, DISPLAY_PORT_NUMBER))
			print("connected")
			self.connection=self.s
		self.connection.setblocking(0) # non-blocking mode
		
		# send capabilities
		self._SendCapabilities()
		self.state="lobby"
	
	## Check if new game start is available. If yes, MenuGod goes to game mode
	# \returns game info if present, else None
	def CheckNewGameStart(self):
		msg=self._GetSpecificMessage("gamestart")
		if msg:
			try:
				if not msg["game"]["mode"] in gamemodes.available_modes.keys():

					raise Exception("I don't know game mode {}. I only know these game modes: {}".format(msg["game"]["mode"],gamemodes.available_modes.keys()))

				self.state="game"
			except Exception as e:
				self.SendError(str(e))
		return msg

	## Send game info (scores). Raises AbortGameException if data received
	def SendGameInfo(self, info):
		assert self.state=="game"
		self._SendJson({"gameinfo":info})
		if self._CheckForMessage():
			self._PopMessage()
			raise AbortGameException()

	## Send available game modes etc.
	def _SendCapabilities(self):
		assert self.state=="init"
		self._SendJson({"capabilities":{"gamemodes":gamemodes.available_modes.keys()}})
	
	## Try to get specific message and throw error is other messages are incoming
	# \returns message if available, None if not
	def _GetSpecificMessage(self,messagekey):
		if self._CheckForMessage():
			msg=self._PopMessage()
			k=msg.keys()
			if len(k)>1:
				self.SendError("more than one key/value pair in message!")
				return None
			if k[0]!=messagekey:
				self.SendError("expected {} message, got {}".format(messagekey, k[0]))
				return None
			return msg[messagekey]
		else:
			return None
	
	## Send error message to menu god
	def SendError(self,error):
		print("menu god protocol ERROR: {}".format(error))
		self._SendJson({"error":error})
	
	## Reads buffer until empty or \0
	# \returns True if new message complete available, else False
	# use popMessage to retrieve the message
	def _CheckForMessage(self):
		if len(self.buffer)>0 and buffer[-1]=="\0": # already a message in the buffer
			return True
		try:
			while(True):
				self.buffer+=self.connection.recv(1)
				if self.buffer[-1]=="\0":
					return True
		except socket.error: # no data available
			return False
	
	## Return currently buffered message and clear the buffer
	def _PopMessage(self):
		j=json.loads(self.buffer[:-1])
		self.buffer=""
		return j

	## Send game over message. After this, no more messages should be sent!
	def GameOver(self):
		self._SendJson({"gameover":None})
		self.state="lobby"
	
	## Internal helper function
	def _SendJson(self,data):
		j=json.dumps(data)+"\0"
		self.connection.send(j)

if __name__=="__main__":
	import time
	m=MenuGod("10.0.0.158")

	if False: # skip gamestart
		print("skipping waiting for gamestart")
		m.state="game"
	else:
		while(True):
			gamestart=m.CheckNewGameStart()
			if gamestart is not None:
				print("starting game with info: {}".format(gamestart))
				break
	try:
		for i in range(10):
			info={
				"scores":{
					"score": {"type":"int","values":[i,i*3]},
					"area": {"type":"bar","values":[0.0,0.0]}
				},
				"consoleoutput":"this is transmission number {}".format(i)
			}
			m.SendGameInfo(info)
			time.sleep(1.0)
	except AbortGameException:
		print("game aborted")
	print("sending gameover...")
	m.GameOver()
	print("end")
