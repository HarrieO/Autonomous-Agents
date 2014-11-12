'''
Group 7
Carla Groenland   10208429
Harrie Oosterhuis 10196129
Fabian Voorter    10218807
'''
import numpy as np

class Agent(object):
	def __init__(self, x_init, y_init, name="Agent"):
		self.x    = x_init
		self.y 	  = y_init
		self.name = name

	# location as tuple
	def loc(self):
		return (self.x,self.y)

	# print location and name
	def printState(self):
		print self.name + "("+ str(self.x) + "," + str(self.y) + ")"

	def sameLocation(self, location):
		return self.x == location[0] and self.y == location[1]

	# location as tuple after movement, move is given as tuple
	def locAfterMove(self, move):
		return ((self.x + move[0])%11, (self.y + move[1])%11)

	# returns list of moves and their probabilities (equal probability for each move)
	def getMoveList(self, stateInfo=None):
		moveList = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
		prob 	 = 1.0/len(moveList)
		return [(prob,move) for move in moveList ]

	# returns list of locations after a move and the probability of each location
	def expand(self, stateInfo=None):
		states = []
		for prob, move in self.getMoveList(stateInfo):
			states.append((prob,self.locAfterMove(move)))
		return states

	# places agent at location
	def setLocation(self, location):
		self.x, self.y = location

	# moves agent, move is a tuple (dx,dy)
	def move(self, move):
		self.x, self.y = self.locAfterMove(move)

	# picks a random move according to getMoveList
	def pickMove(self, stateInfo=None):
		moveList = self.getMoveList(stateInfo)
		pick = np.random.rand()
		for prob, move in moveList:
			if pick <= prob:
				return move
			else:
				pick -= prob
