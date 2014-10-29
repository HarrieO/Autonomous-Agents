import numpy as np

class Agent(object):
	def __init__(self, x_init, y_init, name="Agent"):
		self.x    = x_init
		self.y 	  = y_init
		self.name = name

	def printState(self):
		print self.name + "("+ str(self.x) + "," + str(self.y) + ")"

	def sameLocation(self, location):
		return self.x == location[0] and self.y == location[1]

	def locAfterMove(self, move):
		return ((self.x + move[0])%11, (self.y + move[1])%11)

	def getMoveList(self, stateInfo=None):
		moveList = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
		prob 	 = 1.0/len(moveList)
		return [(prob,move) for move in moveList ]

	def expand(self, stateInfo=None):
		states = []
		for prob, move in self.getMoveList(stateInfo):
			states.append((prob,self.locAfterMove(move)))
		return states

	def setLocation(self, location):
		self.x, self.y = location

	def move(self, move):
		self.x, self.y = self.locAfterMove(move)

	def pickMove(self, stateInfo=None):
		moveList = self.getMoveList(stateInfo)
		pick = np.random.rand()
		for prob, move in moveList:
			if pick <= prob:
				return move
			else:
				pick -= prob
