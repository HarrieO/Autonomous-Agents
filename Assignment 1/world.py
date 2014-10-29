from predator import *
from prey import *

class World(object):
	def __init__(self, prey, predator, width=11, height=11):
		self.width  	= width
		self.height 	= height
		#self.grid   	= [[None for x in range(width)] for y in range(height) ]
		self.prey   	= prey
		self.predator 	= predator

	def prettyPrint(self, worldPrint, printStates):
		if worldPrint:
			print "#" * (self.width*5-1 + 4)
			for y in range(self.height):
				print "#",
				for x in range(self.width):
					if x == self.prey.x and y == self.prey.y:
						print "PREY",
					elif x == self.predator.x and y == self.predator.y:
						print "PRED",
					else:
						print "____",
				print "#"
			print "#" * (self.width*5-1 + 4)
			print
		if printStates:
			self.predator.printState()
			self.prey.printState()
			print


	def stopState(self, move):
		if self.prey.sameLocation(self.predator.locAfterMove(move)):
			return True
		return False

	def run(self, worldPrint=False, printStates=False):
		
		self.prettyPrint(worldPrint,printStates)

		iterations = 0;
		
		predMove = self.predator.pickMove()
		while not self.stopState(predMove):
			self.predator.move(predMove)
			self.prey.move(self.prey.pickMove(self.predator.loc()))
			predMove = self.predator.pickMove()

			self.prettyPrint(worldPrint,printStates)

			iterations += 1

		if worldPrint or printStates:
			print 
			print "Finished after", iterations, "moves."
		return iterations
		