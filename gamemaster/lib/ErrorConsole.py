import socket
import json

ERROR_CONSOLE_PORT_NUMBER = 6000

class ErrorConsole(object):
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
		self.port = ERROR_CONSOLE_PORT_NUMBER

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
				try:
					s.bind(("", self.port))
				except socket.error: # address already in use?
					if self.port == ERROR_CONSOLE_PORT_NUMBER+10:
						self.port = ERROR_CONSOLE_PORT_NUMBER
					else:
						self.port += 1
				s.listen(1)
				s.settimeout(ErrorConsole.CONNECTION_TIMEOUT)
				self.server = s

			# check for new connections on server
			try:
				conn, addr = self.server.accept()
				print("connection from {}".format(addr))
				self.connection = conn
				self.connection.setblocking(0) # non-blocking mode
			except socket.timeout:
				print("timeout - using port {}".format(self.port))

		# client mode
		else:
			print("connecting to {}...".format(self.targetHostname))
			try:
				s = socket.create_connection((self.targetHostname, ERROR_CONSOLE_PORT_NUMBER), 0.01)
				self.connection = s
				print("connected")
				self.connection.setblocking(0) # non-blocking mode
			except socket.timeout:
				print("timeout")
	## Internal helper function
	def _SendJson(self, data):
		if self.connection is None:
			self._TryConnect()
		else:
			j = json.dumps(data)+"\0"
			try:
				self.connection.send(j)
			except socket.error:
				self._CleanupConnections()
	
	def SendStatus(self, busErrorStatistic, socketStatus):
		self._SendJson({"busErrorStatistic":busErrorStatistic, "socketStatus":socketStatus})
