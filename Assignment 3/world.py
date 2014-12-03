import random

class World(object):
	def __init__(self, preyLoc, predatorLocs, width=11, height=11):
		self.width  	= width
		self.height 	= height
		# position is the relative distance between predator and prey
		self.position  	= tuple(sorted(
							tuple(self.relativedist(predLoc[0]-preyLoc[0],predLoc[1]-preyLoc[1]) for predLoc in predatorLocs)
						  ))
		self.no_predator = len(self.position)
		self.singleStates = [((dx,dy)) for dx in range(-(self.width-1)/2,(self.width-1)/2+1) \
		                for dy in range(-(self.height-1)/2,(self.height-1)/2+1) \
		                if (dx,dy) != (0,0) ]
		self.singleStates = [((dx,dy)) for dx in range(-(self.width-1)/2,(self.width-1)/2+1) \
		                for dy in range(-(self.height-1)/2,(self.height-1)/2+1) \
		                if (dx,dy) != (0,0) ]
		self.statePairs = None
		self.allMoves   = None


	# sets state of world to relative position
	def setState(self, position):
		self.position = tuple(sorted(position))

	# list of all potential moves
	def singleMoveList(self):
		return [(0,0),(0,-1),(0,1),(1,0),(-1,0)]

	def allMoveList(self):
		if not self.allMoves:
			singleMoveList = self.singleMoveList()
			movePairs = [(move,) for move in singleMoveList]
			for _ in range(len(self.position)-1):
				newMovePairs = []
				for move in singleMoveList:
					for pair in movePairs:
						newMovePairs.append(pair + (move,))
				movePairs = newMovePairs[:]
			self.allMoves = movePairs
		return self.allMoves


	# list of all possible starting-states, (not the state where the predator is at the preys location)
	def allStates(self):
		if not self.statePairs:
			statePairs = [(state,) for state in self.singleStates]
			for _ in range(len(self.position)-1):
				newStatePairs = []
				for state in self.singleStates:
					for statePair in statePairs:
						if state not in statePair:
							newStatePairs.append(statePair + (state,))
				#print newStatePairs
				statePairs = newStatePairs[:]
			self.statePairs = statePairs
		return self.statePairs

	# returns true if predator is at the same location of the prey
	def stopState(self):
		if (0,0) in self.position:
			return True
		for i, state in enumerate(self.position[:-1]):
			if state in self.position[i+1:]:
				return True
		return False

	# returns element with given probabilities, list should be (elem, prob) pairs probs should sum to 1
	def pickElementWithProbs(self, elemProbList):
		pick = random.random()
		for elem, prob in elemProbList:
			if pick <= prob:
				return elem
			pick -= prob
		return elemProbList[-1][0]
	
	# torialdistance on a dimension given an absolute distance and the span of dimension in the world (width height)
	def toroidaldis(self, distance, span):
		return int((distance+(span-1)/2.0)%11-(span-1)/2.0)

	# returns the relative delta x and delta y given an absolute delta x and delta y
	def relativedist(self, dx, dy):
		return self.toroidaldis(dx,self.width),self.toroidaldis(dy,self.height)

	# relative position after given move, (move performed by predator)
	def posAfterMove(self, moves):
		return tuple(sorted(
			tuple(self.relativedist(self.position[i][0] + moves[i][0],self.position[i][1] + moves[i][1]) for i in range(self.no_predator))
			))

	# moves the predator (move is a tuple (dx,dy))
	def move(self, preymove, predmoves):
		self.position = self.posAfterMove(predmoves)
		if random.random() > 0.2:
			self.preyMove(preymove)
		return self.reward()

	def reward(self):
		for i, state in enumerate(self.position[:-1]):
			if state in self.position[i+1:]:
				return (10,-10)
		if (0,0) in self.position:
			return (-10,10)
		return (0,0)

	# relative position after prey moves
	def posAfterPreyMove(self, move):
		return self.posAfterMove(((-move[0],-move[1]),)*self.no_predator)

	# moves the prey (move is a tuple (dx,dy))
	def preyMove(self, move):
		self.position = self.posAfterPreyMove(move)