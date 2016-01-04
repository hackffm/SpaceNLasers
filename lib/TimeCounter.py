import time

class TimeCounter:

	

	def __init__(self):
		self.endTime = 0
		return None

	def setTimeout(self,timeoutInSec):
		self.endTime = time.time()+timeoutInSec

	def checkTimeout(self):
		self.timeStatus = 0
		deltaTime = time.time() - self.endTime
			
		if deltaTime>0:
			self.timeStatus = 1
		return self.timeStatus