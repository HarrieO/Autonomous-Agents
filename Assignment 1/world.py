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
		world.prettyPrint()
		



world = World(None, None)
print world.prettyPrint()