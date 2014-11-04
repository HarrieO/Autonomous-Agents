from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np

epsilon = 0.01

def evaluatePolicy(policy, discountFactor, values=None):
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	if values is None:
		values = {}
	for predloc in alllocations:
		for preyloc in alllocations:
			if preyloc != predloc:
				values[(predloc,preyloc)] = 0
	delta = 1
	numIt = 0
	while delta > epsilon:
		delta = 0
		newValues = {}
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
				newValues[(predloc,preyloc)] = preySum
				delta = max(delta, np.abs(preySum - temp))
		values = newValues
		numIt +=1
	return values, numIt

def improvePolicy(policy,values, discountFactor):
	stable = True
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	for predloc in alllocations:
		for preyloc in alllocations:
			if predloc == preyloc:
				continue
			prey 	 = Prey(*preyloc)
			oldPolicy = policy[(predloc,preyloc)]
			bestPolicy = (0,0)
			bestVal = 0
			for predMove in moves:
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
				stable = False
	return policy, stable

def iterate_policy(discountFactor):
	# initialize policy
	policy = {}
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	for predloc in alllocations:
		for preyloc in alllocations:
			policy[(predloc,preyloc)] = (0,0)
	stable = False
	values = None
	numIt = 0
	while not stable:
		values, numItEval = evaluatePolicy(policy, discountFactor, values)
		numIt += numItEval
		policy, stable = improvePolicy(policy, values,discountFactor)
		numIt +=1
	return numIt, values
discountFactors = np.array([0.1,0.5,0.7,0.9])
for discountFactor in discountFactors:
	numIt, values = iterate_policy(discountFactor)	
	print "For a discount factor of ", discountFactor, ", ", numIt, " iterations were required for convergence."

values[((5,5),(5,5))]=10

for y in range(11):
	valueList = []
	for x in range(11):
		valueList.append(values[((x,y),(5,5))])
	print valueList