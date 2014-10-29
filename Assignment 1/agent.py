import numpy as np

class Agent(object):
	def __init__(self, x_init, y_init, name="Agent"):
		self.x    = x_init
		self.y 	  = y_init
		self.name = name

	def printState(self):
		print self.name + "("+ str(self.x) + "," + str(self.y) + ")"

	def getMoveList(self, stateInfo=None):
		moveList = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
		prob 	 = 1/len(moveList)
		return [(prob,move) for move in moveList ]

	def expand(self, stateInfo=None):
		states = []
		for prob, move in self.getMoveList(worldState):
			states.append((prob,(self.x+move[0],self.y+move[1])))

	def move(self, step):
		self.x = (self.x+step[0])%11
		self.y = (self.y+step[1])%11

	def pickMove(self, stateInfo):
		moveList = self.getMoveList(stateInfo)
		pick = np.random.rand()
		for prob, move in moveList:
			if pick <= prob:
				return move
			else:
				pick -= prob

	


print Agent(0,1).expand()