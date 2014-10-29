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


	def stopState(self, predatorMove):
		if self.predator.x + predatorMove[0] == self.prey.x and self.predator.y + predatorMove[1] == self.prey.y:
			return True
		return False

	def run(self, worldPrint=False, printStates=False):
		
		self.prettyPrint(worldPrint,printStates)

		iterations = 0;
		
		predMove = self.predator.calculateMove(self)
		while not self.stopState(predMove):
			self.predator.move(predMove)
			self.prey.move(self.prey.calculateMove(self))
			predMove = self.predator.calculateMove(self)

			self.prettyPrint(worldPrint,printStates)

			iterations += 1

		if worldPrint or printStates:
			print 
			print "Finished after", iterations, "moves."
		return iterations
		