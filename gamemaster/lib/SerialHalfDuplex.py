import serial


class SerialHalfDuplex(object):
	def __init__(self, device, baud):
		self._device = device
		self._baud = baud
		self.Init()

	def Init(self):
		print(self._device)
		print(self._baud)
		self._serial = serial.Serial(self._device, self._baud, timeout=0.1) # Requires device/baud and returns an ID

	def SetBuffer(self, buf):
		#print("set buffer={}".format(buffer))
		self._serialBuffer = buf

	def WriteBuffer(self):
		# print(self.__serialBuffer)
		# wiringpi2.digitalWrite(1,1) # set txn pin to write mode
		#print("write buffer={}".format(self.__serialBuffer))
		self._serial.write(self._serialBuffer) # sending buffer
		self._serial.flush()
		#wiringpi2.digitalWrite(1,0) # set txn pin back to read mode

	def Ping(self, ping):
		self.SetBuffer(ping)
		self.WriteBuffer()

	def PingPong(self, ping):
		self.SetBuffer(ping)
		self.WriteBuffer()
		return self._serial.readline()

	def ReadLine(self):
		return self._serial.readline()

	def Close(self):
		self._serial.close()
