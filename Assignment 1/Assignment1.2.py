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

def valueFunction():
	# all locations on the grid
	alllocations = [ (x,y) for x in range(11) for y in range(11)]

	# initialize value function
	values = {}
	for predloc in alllocations:
		for preyloc in alllocations:
			if preyloc != predloc:
				values[(predloc,preyloc)] = 0

	# predator which is placed in the top-left
	agent = Agent(0,0)

	discountFactor = 0.8
	epsilon = 0.01
	delta = 1
	numIt = 0
	while delta > epsilon:
		delta = 0
		newValues = {}
		# sweep over all possible states
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue
				# place predator and prey at location
				agent.setLocation(predloc)
				prey = Prey(*preyloc)
				# temp is previous value of state
				temp = values[(predloc,preyloc)]
				moveSum = 0
				# iterates over each actionthe agent can take
				# and the probability of the action according to the policy
				for prob, newPredloc in agent.expand():
					preySum = 0
					# absorbing state
					if newPredloc == preyloc :
						preySum += 10.0
					else:
						# iterates over the states which the action can lead to, and their probability (stochastic)
						for preyProb, newPreyloc in prey.expand(newPredloc):
							# part of update rule (sum over s')
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]
					# part of update rule (sum over a)
					moveSum += prob * preySum
				# policy evaluation update
				newValues[(predloc,preyloc)] = moveSum
				delta = max(delta, np.abs(moveSum - temp))
		values = newValues
		numIt += 1

	return values, numIt

# displays the values requested by the assignment
predators = [(0,0),(2,3),(2,10),(10,10)]
preys     = [(5,5),(5,4),(10,0),(0,0)]
values,numIt = valueFunction()
print "Number of iterations: ", numIt
for predator, prey in zip(predators,preys):
	value = values[(predator,prey)]
	print "Locations: ", predator, "; ", prey,". Value: ", value
