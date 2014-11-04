from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np

def valueFunction():

	alllocations = [ (x,y) for x in range(11) for y in range(11)]

	values = {}
	for predloc in alllocations:
		for preyloc in alllocations:
			if preyloc != predloc:
				values[(predloc,preyloc)] = 0

	agent = Agent(0,0)

	discountFactor = 0.8
	epsilon = 0.01
	delta = 1
	numIt = 0
	while delta > epsilon:
		delta = 0
		newValues = {}
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue
				agent.setLocation(predloc)
				prey = Prey(*preyloc)

				temp = values[(predloc,preyloc)]
				moveSum = 0
				for prob, newPredloc in agent.expand():
					preySum = 0
					if newPredloc == preyloc :
						preySum += 10.0
					else:
						for preyProb, newPreyloc in prey.expand(newPredloc):
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]
					moveSum += prob * preySum
				#if moveSum > 0:
				#	print predator, prey, moveSum
				newValues[(predloc,preyloc)] = moveSum
				delta = max(delta, np.abs(moveSum - temp))
		values = newValues
		numIt += 1

	return values, numIt


predators = [(0,0),(2,3),(2,10),(10,10)]
preys     = [(5,5),(5,4),(10,0),(0,0)]
values,numIt = valueFunction()
print "Number of iterations: ", numIt
for predator, prey in zip(predators,preys):
	value = values[(predator,prey)]
	print "Locations: ", predator, "; ", prey,". Value: ", value
