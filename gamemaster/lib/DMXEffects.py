import socket

PATTERN = "goto {}\r\n"
PORT = 3100

class DMXEffectManager(object):
	## Create DMXEffectManager
	# \param hostname hostname/ip to connect to. set to None to disable
	def __init__(self, hostname, config):
		self.hostname = hostname
		if self.hostname is not None:
			print("connecting to DMX controller at {}".format(hostname))
			self.socket = socket.create_connection((self.hostname, PORT))
			self.socket.setblocking(0)
		self.config = config
	
	def Effect(self, name):
		try:
			command = self.config["effectMapping"][name]
			print("sending DMX effect {} = {}".format(name, command))
			if self.hostname is not None:
				self.socket.send(PATTERN.format(command))
		except KeyError:
			print("dmx command {} not found -> skipping")
