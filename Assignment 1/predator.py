import numpy as np

class Predator(object):
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def move(self, worldState):
		self.makeRandomMove()

	def makeRandomMove(self):
		randNum = np.floor(np.random.rand()*5)
		if(randNum ==0):
			self.x = (self.x +1)%11
		elif(randNum==1):
			self.x = (self.x -1)%11
		elif(randNum==2):
			self.x = (self.y +1)%11
		elif(randNum==3):
			self.x = (self.y -1)%11

