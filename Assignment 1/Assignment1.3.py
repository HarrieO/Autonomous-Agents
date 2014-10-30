from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np

# initialize policy
policy = {}
alllocations = [ (x,y) for x in range(11) for y in range(11)]
for predloc in alllocations:
	for preyloc in alllocations:
		if preyloc != predloc:
			policy[(predloc,preyloc)] = (0,0)


def evaluatePolicy(policy, values=None):
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	if values is None:
		values = {}
	for predloc in alllocations:
		for preyloc in alllocations:
			if preyloc != predloc:
				values[(predloc,preyloc)] = 0
	deltas = []
	discountFactor = 0.8
	epsilon = 0.1
	delta = 1
	while delta > epsilon:
		delta = 0
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue
				prey 	 = Prey(*preyloc)
				temp = values[(predloc,preyloc)]
				predMove = policy[(predloc,preyloc)]
				newPredloc = ((predloc[0] + predMove[0])%11,(predloc[1] + predMove[1])%11)
				preySum = 0
				if newPredloc == preyloc :
					preySum += 10.0
				else:
					for preyProb, newPreyloc in prey.expand(newPredloc):
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]
				values[(predloc,preyloc)] = preySum
				delta = max(delta, np.abs(preySum - temp))
		deltas.append(delta)

	return values

def improvePolicy(policy,values):
	stable = true
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	for predloc in alllocations:
		for preyloc in alllocations:
			oldPolicy = policy[(predloc,preyloc)]
			bestPolicy = (0,0)
			bestVal = 0
			for predMove in moves
				newPredloc = ((predloc[0] + predMove[0])%11,(predloc[1] + predMove[1])%11)
				preySum = 0
				if newPredloc == preyloc :
					preySum += 10.0
				else:
					for preyProb, newPreyloc in prey.expand(newPredloc):
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]
				if bestVal <= preySum:
					bestVal = preySum
					bestPolicy = predMove
			policy[(predloc,preyloc)]=bestPolicy
			if oldPolicy != bestPolicy:
				stable = false
	return policy, stable
