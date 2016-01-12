
## Class to manage delayed actions similar to setTimeout in JS
class CountdownTimer:
	all_timers=[]
	def __init__(self,action,time):
		assert time>=0
		self.action=action
		self.time=time
		self.done=False

	def Update(self,dt):
		self.time-=dt
		if self.time<0 and not self.done:
			self.action()
			self.done=True
	
	@staticmethod
	def Add(action,time):
		obj=CountdownTimer(action,time)
		all_timers.append(obj)
	
	@staticmethod
	def UpdateAll(dt):
		for timer in all_timers:
			timer.Update(dt)
		all_timers=[timer for timer in all_timers if timer.time>=0]
	
	@staticmethod
	def Remove(obj):
		all_timers.remove(obj)
	
	@staticmethod
	def Clear():
		all_timers=[]
