import os
import time
import pygame

soundFolder = "sounds/set{setnumber}/"

def loadSound(filename):
	print("loading sound: {}".format(filename))
	return pygame.mixer.Sound(filename)

class SoundSet(object):
	def __init__(self, number):
		self.number = number
		params = {"setnumber":number}

		sounds = ["intro", "laser", "gameOver", "targetDestroyed"]
		for s in sounds:
			setattr(self, s, loadSound((soundFolder+"{sound}.wav").format(sound=s, **params)))

		# load as many music tracks as available
		self.mainMusics = []
		i = 0
		while(True):
			filename = (soundFolder+"music_{}.wav").format(i,**params)
			if os.path.exists(filename):
				self.mainMusics.append(loadSound(filename))
				i += 1
			else:
				break
	
	def PlayAndSleep(self, name):
		sound = getattr(self, name)
		sound.play()
		time.sleep(sound.get_length())
	
	## Get main game durations
	# \returns list of (setnumber, set-internal number, duration) tuples
	def GetDurations(self):
		return [(self.number, i, m.get_length()) for i, m in enumerate(self.mainMusics)]
	
class SoundManager(object):
	MUSIC_CHANNEL = 0
	instance = None

	def __init__(self):
		if SoundManager.instance is not None:
			raise Exception("Sound manager is a singleton instance. an instance is already defined!")
		SoundManager.instance = self
		pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=64)
		pygame.mixer.set_num_channels(20)
		pygame.mixer.set_reserved(1) # number of dedicated channels (e.g. music)
		self.musicChannel = pygame.mixer.Channel(SoundManager.MUSIC_CHANNEL)

		self.sets = []
		i = 0
		while(True):
			if os.path.exists(soundFolder.format(setnumber=i)):
				print("loading sound set {}".format(i))
				self.sets.append(SoundSet(i))
				i += 1
			else:
				break
	def GetDurations(self):
		result = []
		for s in self.sets:
			result += s.GetDurations()
		return result

if __name__ == "__main__":
	sm = SoundManager()
	print(sm.GetDurations())
