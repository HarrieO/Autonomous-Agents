from world    import World
from prey     import Prey
from predator import Predator
import numpy as np

values = np.zeros([11,11])

def reward(predator, move, prey):
	if (predator[0]+move[0])%11 == prey.x and (predator[1]+move[1])%11 == prey.y:
		return 10
	return 0

def valueIteration(prey):
	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	discountFactor = 0.8

	epsilon = 0.01
	delta = 0.0
	oldValues = values.copy()
	for y in range(10):
		for x in range(10):
			sumList = np.zeros(len(moves))
			for i in range(len(moves)):
				move = moves[i]
				sumList[i] = reward([x,y], move, prey) + discountFactor*oldValues[x+move[0],y+move[1]]
			maximum =  max(sumList)
			delta = max(delta,np.abs(values[x,y]-maximum))
			values[x,y] = maximum

	while delta >= epsilon:
		oldValues = values.copy()
		for y in range(10):
			for x in range(10):
				sumList = np.zeros(len(moves))
				for i in range(len(moves)):
					move = moves[i]
					sumList[i] = reward([x,y], move, prey) + discountFactor*oldValues[x+move[0],y+move[1]]
				maximum =  max(sumList)
				delta = max(delta,np.abs(values[x,y]-maximum))
				values[x,y] = maximum

	def policy(state):
		sumList = np.zeros(len(moves))
		for i in range(len(moves)):
			move = moves[i]
			sumList[i] = reward(predator, move, prey) + discountFactor*values[state[0]+move[0],state[1]+move[1]]
		bestIndex = np.argmax(sumList)
		return moves[bestIndex]

	return policy
prey = Prey(5,5)
p = valueIteration(prey)
print p([0,0])