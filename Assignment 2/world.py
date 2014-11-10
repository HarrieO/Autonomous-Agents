import random

class World(object):
	def __init__(self, preyLoc, predatorLoc, width=11, height=11):
		self.width  	= width
		self.height 	= height
		# position is the relative distance between predator and prey
		self.position  	= self.relativedist(predatorLoc[0]-preyLoc[0],predatorLoc[1]-preyLoc[1])

	# sets state of world to relative position
	def setState(self, position):
		self.position = position

	# list of all potential moves
	def moveList(self):
		return [(0,0),(0,-1),(0,1),(1,0),(-1,0)]

	# list of all possible starting-states, (not the state where the predator is at the preys location)
	def allStates(self):
		return [(dx,dy) for dx in range(-(self.width-1)/2,(self.width-1)/2+1) \
		                for dy in range(-(self.height-1)/2,(self.height-1)/2+1) \
		                if (dx,dy) != (0,0) ]

	# returns true if predator is at the same location of the prey
	def stopState(self):
		return self.position == (0,0)

	# returns element with given probabilities, list should be (elem, prob) pairs probs should sum to 1
	def pickElementWithProbs(self, elemProbList):
		pick = random.random()
		for elem, prob in elemProbList:
			if pick <= prob:
				return elem
			pick -= prob
	
	# torialdistance on a dimension given an absolute distance and the span of dimension in the world (width height)
	def toroidaldis(self, distance, span):
		return int((distance+(span-1)/2.0)%11-(span-1)/2.0)

	# returns the relative delta x and delta y given an absolute delta x and delta y
	def relativedist(self, dx, dy):
		return self.toroidaldis(dx,self.width),self.toroidaldis(dy,self.height)

	# relative position after given move, (move performed by predator)
	def posAfterMove(self, move):
		return self.relativedist(self.position[0] + move[0],self.position[1] + move[1])

	# moves the predator (move is a tuple (dx,dy))
	def move(self, move):
		self.position = self.posAfterMove(move)

	# relative position after prey moves
	def posAfterPreyMove(self, move):
		return self.posAfterMove((-move[0],-move[1]))

	# moves the prey (move is a tuple (dx,dy))
	def preyMove(self, move):
		self.position = self.posAfterPreyMove(move)

	# return list of moves the prey can make, and a list of probabilities of each move
	def preyMoves(self):
		moveList = [(0,-1),(0,1),(1,0),(-1,0)]
		for i, move in enumerate(moveList):
			if self.posAfterPreyMove(move) == (0,0):
				del moveList[i]
		probs = [0.2/len(moveList)]*len(moveList)
		return zip([(0,0)] + moveList, [0.8] + probs)

	# list of states after preymove with each probability
	def nextPreyStates(self):
		return [(self.posAfterPreyMove(move), prob) for move, prob in self.preyMoves()]

	# performs a random prey move according to probability distribution of preyMoves
	def performPreyMove(self):
		self.position = self.pickElementWithProbs(self.nextPreyStates())
