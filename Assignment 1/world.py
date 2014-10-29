from predator import *
from prey import *

class World(object):
	def __init__(self, prey, predator, width=11, height=11):
		self.width  	= width
		self.height 	= height
		self.grid   	= [[None for x in range(width)] for y in range(height) ]
		self.prey   	= prey
		self.predator 	= predator

	def prettyPrint(self):
		for row in self.grid:
			print row

	def stopState(self, predatorMove):
		return false

	def run(self):
		self.prettyPrint()
		self.prey.move(self)
		self.predator.move(self)
		



world = World(Prey(0,0), Predator(5,5))
print world.run();