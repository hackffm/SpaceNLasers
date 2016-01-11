import time

from lib.TimeCounter import TimeCounter

import Events
import BusFactory

## Base class for gamemode target AIs
class Target:
	def __init__(self,hwTarget):
		self.hardwareTarget=hwTarget
		self.buffer=[]

	## Called from game engine when this target has been hit.
	# \param event a TargetHitEvent
	def Hit(self,event):
		raise NotImplementedError()

	## Return a list of all buffered bus commands.
	def CollectSerialBuffer(self):
		tmp=self.buffer
		self.buffer=[]
		return tmp

	## Do game mode specific stuff
	def Update(self,dt):
		raise NotImplementedError()

	## Write new color command for target to the target queue
	def setColor(self,color):
		self.buffer.append(BusFactory.setTargetColor(self.hardwareTarget.groupID,self.hardwareTarget.id,color))
	
	## Put effect to the target queue
	def Effect(self,name,*args):
		#try:
			self.buffer.append(self.hardwareTarget.getEffect(name,*args))
		#except KeyError:
		#	print("skipping effect {}".format(name))
