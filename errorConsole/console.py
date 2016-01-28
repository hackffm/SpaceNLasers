#!/usr/bin/python
import socket
import time
import argparse
from collections import defaultdict
import json
import wiringpi2

parser = argparse.ArgumentParser(description="SpaceNLasers game master")
parser.add_argument("gamemaster", type=str, help="IP of gamemaster to connect to")
args = parser.parse_args()

PORT = 6000
ALARM_PIN = 7

CONNECTION_TIMEOUT = 1.0
BUS_ERROR_THRESHOLD = 100
RECEIVE_TIMEOUT_THRESHOLD = 30 # RTT*CONNECTION_TIMEOUT = total timeout in seconds



def alarm(text):
	print("="*80)
	print(text)
	print("="*80)
	print("hit [Enter] to reset alarm")
	wiringpi2.digitalWrite(ALARM_PIN, 1)
	raw_input()
	wiringpi2.digitalWrite(ALARM_PIN, 0)

class DisconnectError(BaseException):
	pass

class UnableToConnectError(BaseException):
	pass

class ReceiveTimeoutError(BaseException):
	pass

class ErrorConsole(object):
	def readBuf(self):
		buffer = ""
		timeoutCounter = 0
		while(True):
			try:
				buf = self.con.recv(1)
				if len(buf) == 0: # disconnected
					raise DisconnectError()
				if buf == "\0":
					return buffer
				buffer += buf
			except socket.error: # no data available
				timeoutCounter += 1
				if timeoutCounter > RECEIVE_TIMEOUT_THRESHOLD:
					raise ReceiveTimeoutError()
				print("sleeping")


	def __init__(self, args):
		self.con = None
		while(True):
			try:
				if self.con is None:
					print("connecting...")
					for port in range(PORT,PORT+10):
						try:
							self.con = socket.create_connection((args.gamemaster, port), CONNECTION_TIMEOUT)
							break
						except BaseException as e:
							print("unable to connect to port {}".format(port))
					else:
						raise UnableToConnectError()
					self.lastBusErrors = defaultdict(lambda: 0)
					print("connected at port {}".format(port))
			
				while(True):
					msg = json.loads(self.readBuf())
					self.analyzeBusErrors(msg)

			except DisconnectError:
				self.con = None
				alarm("network disconnect")
			except ReceiveTimeoutError:
				alarm("no status updates received for {} seconds".format(RECEIVE_TIMEOUT_THRESHOLD*CONNECTION_TIMEOUT))

			except UnableToConnectError:
				delay = 5.0
				print("unable to connect! retrying in {} seconds".format(delay))
				time.sleep(delay)


	def analyzeBusErrors(self,msg):
		busErrors = msg["busErrorStatistic"]
		busErrorDiff = {id: (busErrors[id]-self.lastBusErrors[id]) for id in busErrors}
		for id, newErrors in busErrorDiff.iteritems():
			if newErrors >= BUS_ERROR_THRESHOLD:
				self.lastBusErrors.update(busErrors)
				alarm("bus node {} produced {} errorneous responses!".format(id, newErrors))
	
	def analyzeSocketErrors(self, msg):
		socketStatus = msg["socketStatus"]
		for name, ok in socketStatus.iteritems():
			if not ok:
				alarm("{} disconnected!".format(name))

def main():
	wiringpi2.wiringPiSetup()
	wiringpi2.pinMode(ALARM_PIN, 1)
	ec = ErrorConsole(args)

main()
