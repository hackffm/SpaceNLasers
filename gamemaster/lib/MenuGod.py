import socket
import json
import gamemodes
from SoundManager import SoundManager

# menugod connects to gamemaster
# g->m capabilities
# gamemaster goes to lobby mode
# m->g gamestart: playernames, colors, gamemode, duration
# game starts
# g->m (continuous) gameinfo: scores, consoleoutput
# m->g (optional) abort: -
# g->m gameover: -
# gamemaster goes to lobby mode

## \defgroup menugodMessages MenuGod messages
# Messages sent between the gamemaster and a menugod instance
# \{
# \page capabilities Capabilities of this GameMaster
# \code
# "capabilities": {
# 	"gamemodes":["domination"],
# 	"durations":[90.0, 120.0]
# }
# \endcode
#
# \page gamestart Start a game
# duration is an index for the capabilities::durations array
# \code
# "gamestart": {
# 	"players": [
# 		{"name":"Player1","color":"00FF00"},
# 		{"name":"Player2","color":"FF0000"}
# 	],
# 	"game": {"mode":"domination","duration":0}
# }
# \endcode
#
# \page gameinfo Continuous information about current game state
# \code
# "gameinfo":{
# 	"scores":{
# 		"score": {"type":"int","values":[200,182]},
# 		"area": {"type":"bar","values":[0.3,0.25]}
# 	},
# 	"consoleoutput":{"blablabla"}
# }
# \endcode
#
# \page abort Abort a game
# \warning any menugod->gamemaster communication aborts!
#
# \code
# "abort":0
# \endcode
#
# \page gameover The game is over. Use last \ref gamestart data as score
# \code
# "gameover":0
# \endcode
#
# \page error protocol or state machine error
# \code
# "error":"error text"
# \endcode
# \}

DISPLAY_PORT_NUMBER = 5000

## Exception which is thrown if fully received message is available during game (all message transmissions mean "abort")
class AbortGameException(BaseException):
	pass

class FakeMenuGod(object):
	def __init__(self):
		pass
	def CheckNewGameStart(self):
		return {
			"players":
			[
				{"name":"orange", "color":"FF4000"},
				{"name":"green", "color":"00FF00"}
			],
			"game":
			{
				"mode":"shootingGallery", "duration":0
			},
			"consoleoutput":"starting"
		}
	def SendNewGameStart(self, msg):
		pass
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
class MenuGod(object):
	## Time to try to establish a new connection
	CONNECTION_TIMEOUT = 0.1

	## Initialises state and sends player information to display.
	# \param targetHostname IP of server to connect to. Use empty string to use server-mode
	def __init__(self, targetHostname):
		self.state = "init"

		self.buffer = ""

		self.server = None
		self.connection = None
		self.targetHostname = targetHostname
		self._TryConnect()
	
	def _CleanupConnections(self):
		print("disconnect!")
		self.server = None
		self.connection = None

	## Try to connect to remote host.
	# If connection succeeds, internal state is updated accordingly.
	def _TryConnect(self):
		# server mode
		if self.targetHostname is "":
			# if server is not already running, start it
			if self.server is None:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				print("server mode: waiting for connection...")
				s.bind(("", DISPLAY_PORT_NUMBER))
				s.listen(1)
				s.settimeout(MenuGod.CONNECTION_TIMEOUT)
				self.server = s

			# check for new connections on server
			try:
				conn, addr = self.server.accept()
				print("connection from {}".format(addr))
				self.connection = conn
				self.connection.setblocking(0) # non-blocking mode
				self._SendCapabilities()
			except socket.timeout:
				print("timeout")

		# client mode
		else:
			print("connecting to {}...".format(self.targetHostname))
			try:
				s = socket.create_connection((self.targetHostname, DISPLAY_PORT_NUMBER), MenuGod.CONNECTION_TIMEOUT)
				self.connection = s
				print("connected")
				self.connection.setblocking(0) # non-blocking mode
				self._SendCapabilities()
			except socket.timeout:
				print("timeout")

		# send capabilities
	pass

	## Check if new game start is available. If yes, MenuGod goes to game mode
	# \returns game info if present, else None
	def CheckNewGameStart(self):
		msg = self._GetSpecificMessage("gamestart")
		if msg:
			try:
				if msg["game"]["mode"] not in gamemodes.availableModes.keys():

					raise KeyError("I don't know game mode {}. I only know these game modes: {}".format(msg["game"]["mode"], gamemodes.availableModes.keys()))

				self.state = "game"
			except KeyError as e:
				self.SendError(str(e))
		return msg

	## Send gamestart. Only used for beamer
	def SendNewGameStart(self, msg):
		self._SendJson({"gamestart":msg})

	## Send game info (scores). Raises AbortGameException if data received
	def SendGameInfo(self, info):
		self._SendJson({"gameinfo":info})
		if self._CheckForMessage():
			self._PopMessage()
			raise AbortGameException()

	## Send available game modes etc.
	def _SendCapabilities(self):
		self._SendJson({"capabilities":
			{
				"gamemodes":gamemodes.availableModes.keys(),
				"durations":[duration for _,_,duration in SoundManager.instance.GetDurations()]
			}})

	## Try to get specific message and throw error is other messages are incoming
	# \returns message if available, None if not
	def _GetSpecificMessage(self, messagekey):
		if self._CheckForMessage():
			msg = self._PopMessage()
			k = msg.keys()
			if len(k) > 1:
				self.SendError("more than one key/value pair in message!")
				return None
			if k[0] != messagekey:
				self.SendError("expected {} message, got {}".format(messagekey, k[0]))
				return None
			return msg[messagekey]
		else:
			return None

	## Send error message to menu god
	def SendError(self, error):
		print("menu god protocol ERROR: {}".format(error))
		self._SendJson({"error":error})

	## Reads buffer until empty or \0
	# \returns True if new message complete available, else False
	# use popMessage to retrieve the message
	def _CheckForMessage(self):
		if self.connection is None:
			self._TryConnect()
			return False
		if len(self.buffer) > 0 and self.buffer[-1] == "\0": # already a message in the buffer
			return True
		try:
			while(True):
				print(self.connection.gettimeout())
				buf = self.connection.recv(1)
				if len(buf) == 0: # this will only occur on disconnects. if no data is available, a socket.error will be raised and handled below!
					self._CleanupConnections()
					return False
				self.buffer += buf
				if len(self.buffer) > 0 and self.buffer[-1] == "\0":
					return True
		except socket.error: # no data available
			return False

	## Return currently buffered message and clear the buffer
	def _PopMessage(self):
		j = json.loads(self.buffer[:-1])
		self.buffer = ""
		return j

	## Send game over message. After this, no more messages should be sent!
	def GameOver(self):
		self._SendJson({"gameover":None})
		self.state = "lobby"

	## Internal helper function
	def _SendJson(self, data):
		if self.connection is None:
			self._TryConnect()
		else:
			j = json.dumps(data)+"\0"
			print("sending...")
			self.connection.send(j)
			print("sent!")

