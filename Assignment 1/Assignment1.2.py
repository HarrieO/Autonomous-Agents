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

	deltas = []
	discountFactor = 0.8
	epsilon = 0.01
	delta = 1
	while delta > epsilon:
		delta = 0
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue

				agent.setLocation(predloc)
				prey 	 = Prey(*preyloc)

				temp = values[(predloc,preyloc)]
				moveSum = 0
				for prob, newPredloc in agent.expand():
					preySum = 0
					for preyProb, newPreyloc in prey.expand(newPredloc):
						if newPredloc == preyloc :
							preySum += preyProb * 10
						else:
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]

					moveSum += prob * (preySum)
				#if moveSum > 0:
				#	print predator, prey, moveSum
				values[(predloc,preyloc)] = moveSum
				delta = max(delta, moveSum - temp)
		deltas.append(delta)

	return values, deltas


predators = [(0,0),(2,3),(2,10),(10,10)]
preys     = [(5,5),(5,4),(10,0),(0,0)]


for predator, prey in zip(predators,preys):
	value = valueFunction()[0][(predator,prey)]
	print predator, prey, value


