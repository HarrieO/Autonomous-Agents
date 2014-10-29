from world    import World
from prey     import Prey
from predator import Predator
import numpy as np


def reward(predator, move, prey):
	if (predator[0]+move[0])%11 == prey.x and (predator[1]+move[1])%11 == prey.y:
		return 10
	return 0


def valueGrid(prey):
	values = [ [ 0 for y in range(11) ] for x in range(11)]

	epsilon = 0.001
	delta = epsilon*2

	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	probs  = [0.2, 0.2, 0.2, 0.2, 0.2]

	predator = Predator(5,5)
	prey = Prey(0,0)

	discountFactor = 0.8

	while delta > epsilon:
		delta = 0
		for y in range(11):
			for x in range(11):
				temp = values[x][y]
				moveSum = 0
				for move, prob in zip(moves,probs):
					moveSum += prob * (reward((x,y), move, prey) + discountFactor*values[x][y])
				values[x][y] = moveSum
				delta = max(delta, values[x][y] - temp)

	return values

print valueGrid((5,5))


