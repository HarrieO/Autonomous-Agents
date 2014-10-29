import numpy as np

class Prey(object):
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def move(self, step):
		self.x = (self.x+step[0])%11
		self.y = (self.x+step[1])%11	

	def calculateMove(self, worldState):
		return self.calculateRandomMove(worldState)

	def printState(self):
		print "Prey("+ str(self.x) + "," + str(self.y) + ")"

	def calculateRandomMove(self, worldState):
		(predX,predY) = (worldState.predator.x,worldState.predator.y)
		moveList = [(0,-1),(0,1),(1,0),(-1,0),(0,0)]
		# remove invalid moves
		for i in range(len(moveList))
			coords = moveList.pop(i)
			if ((self.x+coords[0])%11==predX)&&((self.y+coords[1])%11==predY):
				del moveList[i]
		randNum = np.floor(np.random.rand()*5)
		# calculate random move
		if(randNum ==0):
			secondNum = np.floor(np.random.rand()*(len(moveList)-1))
			return moveList[secondNum]
		else:
			return moveList[-1]
