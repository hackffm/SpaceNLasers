
## Class to manage delayed actions similar to setTimeout in JS
class CountdownTimer:
	all_timers=[]
	def __init__(self,action,time,loop=False):
		assert time>=0
		self.action=action
		self.time=time
		self.done=False
		self.originalTime=time if loop else None

	def Update(self,dt):
		self.time-=dt
		if self.time<0 and not self.done:
			self.action()
			if self.originalTime is None:
				self.done=True
			else: # loop
				self.time+=self.originalTime
	
	@staticmethod
	def Add(action,time,**kwargs):
		obj=CountdownTimer(action,time,**kwargs)
		CountdownTimer.all_timers.append(obj)
	
	@staticmethod
	def UpdateAll(dt):
		for timer in CountdownTimer.all_timers:
			timer.Update(dt)
		CountdownTimer.all_timers=[timer for timer in CountdownTimer.all_timers if timer.time>=0]
	
	@staticmethod
	def Remove(obj):
		CountdownTimer.all_timers.remove(obj)
	
	@staticmethod
	def Clear():
		CountdownTimer.all_timers=[]
