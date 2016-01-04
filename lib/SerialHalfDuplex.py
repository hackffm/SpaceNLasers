import serial          
import wiringpi2


class SerialHalfDuplex:
	# def __init__(self):
		# self.initSerialGPIO()

	def initSerialGPIO(self):
		wiringpi2.wiringPiSetup()
		wiringpi2.pinMode(1,1) # pin mode to output for serial txn (half duplex direction)
		wiringpi2.digitalWrite(1,0) # set txn to read

	def configSerial(self,device,baud):
		self.__device = device
		self.__baud = baud
		self.Init()

	def Init(self):
		print(self.__device)
		print(self.__baud)
		self.__serial = serial.Serial(self.__device, self.__baud,timeout=0.1) # Requires device/baud and returns an ID

	def SetBuffer(self,buffer):
		#print("set buffer={}".format(buffer))
		self.__serialBuffer = buffer

	def WriteBuffer(self):
		# print(self.__serialBuffer)
		# wiringpi2.digitalWrite(1,1) # set txn pin to write mode
		#print("write buffer={}".format(self.__serialBuffer))
		self.__serial.write(self.__serialBuffer) # sending buffer
		self.__serial.flush()
		#wiringpi2.digitalWrite(1,0) # set txn pin back to read mode

	def Ping(self,ping):
		self.SetBuffer(ping)
		self.WriteBuffer()

	def PingPong(self,ping):
		self.SetBuffer(ping)
		self.WriteBuffer()
		return self.__serial.readline()

	def ReadLine(self):
		return self.__serial.readline()

	def Close(self):
		self.__serial.close()