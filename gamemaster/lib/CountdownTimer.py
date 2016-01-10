
## Class to manage delayed actions similar to setTimeout in JS
class CountdownTimer:
	def __init__(self,action,time):
		assert time>0
		self.action=action
		self.time=time
		self.done=False

	def Update(self,dt):
		self.time-=dt
		if self.time<0 and not self.done:
			self.action()
			self.done=True
