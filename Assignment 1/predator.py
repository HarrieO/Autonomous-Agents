import numpy as np

class Predator(object):
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def move(self, step):
		self.x = (self.x+step[0])%11
		self.y = (self.x+step[1])%11

	def calculateMove(self, worldState):
		return self.makeRandomMove()

	def calculateRandomMove(self):
		randNum = np.floor(np.random.rand()*5)
		if(randNum ==0):
			return (0,1)
		elif(randNum==1):
			return (0,-1)
		elif(randNum==2):
			return (1,0)
		elif(randNum==3):
			return (-1,0)
		else:
			return (0,0)

