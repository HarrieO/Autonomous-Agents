from world    import World
from prey     import Prey
from predator import Predator
import numpy as np

values = np.zeros([11,11])


def reward(predator, move, prey):
	if predator.x+move[0] == prey.x and predator.y+move[1] == prey.y:
		return 10
	return 0

moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
predator = Predator()

discountFactor = 0.8

epsilon = 0.01
delta = 2.0*epsilon
while delta >= epsilon:
	oldValues = values.copy()
	for y in range(11):
		for x in range(11):
			sumList = np.zeros(len(moves))
			for i in range(len(moves)):
				move = moves[i]
				sumList[i] =reward(predator, move, prey) + discountFactor*oldValues[x+move[0],y+move[1]]
			maximum =  max(sumList)
			delta = max(delta,np.abs(values[x,y]-maximum))
			values[x,y] = maximum

def policy(state):
	sumList = np.zeros(len(moves))
	for i in range(len(moves)):
		move = moves[i]
		sumList[i] =reward(predator, move, prey) + discountFactor*values[x+move[0],y+move[1]]
	bestIndex = np.argmax(sumList)
	return moves[bestIndex]