from world    import World
from prey     import Prey
from predator import Predator
import numpy as np


def reward(predator, move, prey):
	if (predator[0]+move[0])%11 == prey[0] and (predator[1]+move[1])%11 == prey[1]:
		return 10
	return 0

def preyMoveList(prey, predator):
	moveList = [(0,1),(0,-1),(1,0),(-1,0)]
	for i in range(len(moveList)):
		move = moveList[i]
		if prey[0] + move[0] == predator[0] and prey[1] + move[1] == predator[1]:
			del moveList[i]
			break
	probs = [0.2/len(moveList)] * len(moveList)

	moveList.append((0,0))
	probs.append(0.8)

	return moveList, probs






def valueFunction():

	allLocations = [ (x,y) for x in range(11) for y in range(11)]

	values = {}
	for predator in allLocations:
			for prey in allLocations:
				values[(predator,prey)] = 0

	predMoves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	predProbs  = [0.2, 0.2, 0.2, 0.2, 0.2]

	deltas = []
	discountFactor = 0.8
	epsilon = 0.01
	delta = 1
	while delta > epsilon:
		delta = 0
		for predator in allLocations:
			for prey in allLocations:
				if predator[0] == prey[0] and predator[1] == prey[1]:
					continue
				temp = values[(predator,prey)]
				moveSum = 0
				for move, prob in zip(predMoves,predProbs):
					preySum = 0
					for preyMove, preyProb in zip(*preyMoveList(prey,predator)):
						newPrey = ((prey[0] + preyMove[0])%11, (prey[1] + move[1])%11)
						preySum += preyProb * (reward(predator, move, prey) + discountFactor * values[(predator,newPrey)])

					moveSum += prob * (preySum)
				#if moveSum > 0:
				#	print predator, prey, moveSum
				values[(predator,prey)] = moveSum
				delta = max(delta, moveSum - temp)
		deltas.append(delta)

	return values, deltas


predators = [(0,0),(2,3),(2,10),(10,10)]
preys     = [(5,5),(5,4),(10,0),(0,0)]


for predator, prey in zip(predators,preys):
	value = valueFunction()[0][(predator,prey)]
	print predator, prey, value


