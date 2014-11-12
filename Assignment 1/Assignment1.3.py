'''
Group 7
Carla Groenland   10208429
Harrie Oosterhuis 10196129
Fabian Voorter    10218807
'''
from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np

epsilon = 0.01

def evaluatePolicy(policy, discountFactor, values=None):
	# all locations on the grid
	alllocations = [ (x,y) for x in range(11) for y in range(11)]

	# initialize values if None is given
	if values is None:
		values = {}
	for predloc in alllocations:
		for preyloc in alllocations:
			if preyloc != predloc:
				values[(predloc,preyloc)] = 0
	delta = 1
	numIt = 0
	# perform update values according to given pseudo-code
	while delta > epsilon:
		delta = 0
		newValues = {} # will be filled with new values
		# loop over all states
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc: # impossible state
					continue
				prey 	 = Prey(*preyloc)
				temp = values[(predloc,preyloc)]
				predMove = policy[(predloc,preyloc)]
				# make move according to policy
				newPredloc = ((predloc[0] + predMove[0])%11,(predloc[1] + predMove[1])%11)
				preySum = 0
				# calculate discounted sum
				if newPredloc == preyloc :
					preySum += 10.0 # game ends after this
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
	# all locations in the grid and all possible moves
	alllocations = [ (x,y) for x in range(11) for y in range(11)]
	moves = [(0,0),(0,1),(0,-1),(1,0),(-1,0)]
	# loop over possible states
	for predloc in alllocations:
		for preyloc in alllocations:
			if predloc == preyloc:
				continue
			prey 	 = Prey(*preyloc)
			oldPolicy = policy[(predloc,preyloc)]
			bestPolicy = (0,0)
			bestVal = 0
			# calculate greedy policy according to values
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
			# keep track of whether the policy is adjusted
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
	# update policy and values until the policy is unaltered
	while not stable:
		values, numItEval = evaluatePolicy(policy, discountFactor, values)
		numIt += numItEval
		policy, stable = improvePolicy(policy, values,discountFactor)
		numIt +=1
	return numIt, values

# compare iterations required for convergence 
discountFactors = np.array([0.1,0.5,0.7,0.9])
for discountFactor in discountFactors:
	numIt, values = iterate_policy(discountFactor)	
	print "For a discount factor of ", discountFactor, ", ", numIt, " iterations were required for convergence."

# this state can not be reached, (predator and prey share location)
values[((5,5),(5,5))]=0

# display all values for predator positions if prey has position (5,5)
for y in range(11):
	valueList = []
	for x in range(11):
		valueList.append(values[((x,y),(5,5))])
	print valueList