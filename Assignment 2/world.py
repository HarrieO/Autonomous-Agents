from agent import *
from prey import *

class World(object):
	def __init__(self, preyLoc, predatorLoc, width=11, height=11):
		self.width  	= width
		self.height 	= height
		# position is the relative distance between predator and prey
		self.position  	= self.relativedist(predatorLoc[0]-preyLoc[0],predatorLoc[1]-preyLoc[1])
	
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