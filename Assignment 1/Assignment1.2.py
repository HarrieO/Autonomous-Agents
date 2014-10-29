from world    import World
from prey     import Prey
from predator import Predator
import numpy as np


def reward(predator, move, prey):
	if (predator[0]+move[0])%11 == prey[0] and (predator[1]+move[1])%11 == prey[1]:
		return 10
	return 0


def valueGrid(prey):
	values = [ [ 0 for y in range(11) ] for x in range(11)]

	epsilon = 0.1
	delta = epsilon*2

	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	probs  = [0.2, 0.2, 0.2, 0.2, 0.2]

	discountFactor = 0.8
	deltas = []

	while delta > epsilon:
		delta = 0
		for y in range(11):
			for x in range(11):
				temp = values[x][y]
				moveSum = 0
				for move, prob in zip(moves,probs):
					nx, ny = (x + move[0])%11, (y + move[1])%11 
					moveSum += prob * (reward((x,y), move, prey) + discountFactor*values[nx][ny])
				values[x][y] = moveSum
				delta = max(delta, values[x][y] - temp)
	return values, deltas

predators = [(0,0),(2,3),(2,10),(10,10)]
preys     = [(5,5),(5,4),(10,0),(0,0)]


for predator, prey in zip(predators,preys):
	print valueGrid(prey)[predator[0]][predator[1]]


