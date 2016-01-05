class TargetHitRecord:
	weapon = ''
	hitPoint = 5 # default hit point
	hitType = 'laser' # default hit type 

	def __init__(self,weapon,hitPoint,hitType):
		self.weapon = weapon
		self.hitPoint = hitPoint
		self.hitType = hitType