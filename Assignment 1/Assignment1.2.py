from world    import World
from prey     import Prey
from predator import Predator
import numpy as np


def reward(predator, move, prey):
	if predator.x+move[0] == prey.x and predator.y+move[1] == prey.y:
		return 10
	return 0

values = [ [ 0 for y in range(11) ] for x in range(11)]

epsilon = 0.1
delta = epsilon*2

moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
prob  = [0.2, 0.2, 0.2, 0.2, 0.2]

predator = Predator()

discountFactor = 0.8

while delta > epsilon:
	valuesOld = [row[:] for row in values]
	for y in range(11):
		for x in range(11):
			temp = values[x][y]
			moveSum = 0
			for move, prob in moves:
				moveSum += prob * ()


