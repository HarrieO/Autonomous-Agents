import numpy as np

class Prey(object):
	def __init__(self, x_init, y_init):
		self.x = x_init
		self.y = y_init

	def move(self, step):
		self.x = (self.x+step[0])%11
		self.y = (self.y+step[1])%11	

	

	def calculateMove(self, worldState):
		return self.calculateRandomMove(worldState)

	def printState(self):
		print "Prey("+ str(self.x) + "," + str(self.y) + ")"

	def calculateRandomMove(self, worldState):
		if np.floor(np.random.rand()*5) > 0:
			return (0,0)

		predX,predY = (worldState.predator.x,worldState.predator.y)
		moveList = [(0,-1),(0,1),(1,0),(-1,0)]
		# remove invalid moves
		for i in range(len(moveList)):
			coords = moveList[i]
			if ((self.x+coords[0])%11==predX) and ((self.y+coords[1])%11==predY):
				del moveList[i]
				break
		
		secondNum = int( np.floor(np.random.rand()*len(moveList)) )
		return moveList[secondNum]
		
