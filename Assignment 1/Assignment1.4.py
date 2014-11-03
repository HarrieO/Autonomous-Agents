from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np
import time

def valueIteration():

	alllocations = [ (x,y) for x in range(11) for y in range(11)]

	values = {}
	bestMoves = {}
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
		newValues = {}
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue
				agent.setLocation(predloc)
				prey = Prey(*preyloc)
				temp = values[(predloc,preyloc)]
				bestVal = 0
				bestMove = (0,0)
				for prob, predMove in agent.getMoveList():
					preySum = 0
					newPredloc = ((predloc[0] + predMove[0])%11,(predloc[1] + predMove[1])%11)
					if newPredloc == preyloc :
						preySum += 10.0
					else:
						for preyProb, newPreyloc in prey.expand(newPredloc):
							preySum += preyProb * discountFactor * values[(newPredloc,newPreyloc)]
					if bestVal <= preySum:
						bestVal = preySum
						bestMove = predMove
				newValues[(predloc,preyloc)] = bestVal
				bestMoves[(predloc,preyloc)] = bestMove
				delta = max(delta, np.abs(bestVal - temp))
		values = newValues
		deltas.append(delta)

	def policy(state):
		predloc, preyloc = state
		agent.setLocation(predloc)
		prey = Prey(*preyloc)
		return bestMoves[(predloc,preyloc)]
	return policy

start = time.time()
policy = valueIteration()
print "Time taken", round((time.time()-start)*10000)/100, "seconds"

print policy(((0,1),(0,2)))
print policy(((0,2),(0,0)))
print policy(((0,0),(5,5)))