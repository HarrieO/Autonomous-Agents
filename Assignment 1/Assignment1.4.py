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
import time

def valueIteration(discountFactor):
	# all locations in grid
	alllocations = [ (x,y) for x in range(11) for y in range(11)]

	# initialize values
	values = {}
	bestMoves = {}
	for predloc in alllocations:
			for preyloc in alllocations:
				if preyloc != predloc:
					values[(predloc,preyloc)] = 0

	agent = Agent(0,0)

	deltas = []
	epsilon = 0.01
	delta = 1
	numIt = 0
	# perform value iteration according to pseud-code
	while delta > epsilon:
		delta = 0
		newValues = {}
		# loop over all states
		for predloc in alllocations:
			for preyloc in alllocations:
				if predloc == preyloc:
					continue
				agent.setLocation(predloc)
				prey = Prey(*preyloc)
				temp = values[(predloc,preyloc)]
				# find optimal value according to current values
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
		numIt+=1
	# greedy policy to the optimal values computed above
	def policy(state):
		predloc, preyloc = state
		agent.setLocation(predloc)
		prey = Prey(*preyloc)
		return bestMoves[(predloc,preyloc)]
	return numIt, values, policy

# compare iterations required for convergence 
discountFactors = np.array([0.1,0.5,0.7,0.9])
for discountFactor in discountFactors:
	numIt, values,_ = valueIteration(discountFactor)	
	print "For a discount factor of ", discountFactor, ", ", numIt, " iterations were required for convergence."


# this state can not be reached, (predator and prey share location)
values[((5,5),(5,5))]=0

# display all values for predator positions if prey has position (5,5)
for y in range(11):
	valueList = []
	for x in range(11):
		valueList.append(values[((x,y),(5,5))])
	print valueList

# time valueIteration for assignment 1.5
start = time.time()
_,_,policy=valueIteration(0.8)
print "Time taken", round((time.time()-start)*10000)/100, "seconds"

print policy(((0,1),(0,2)))
print policy(((0,2),(0,0)))
print policy(((0,0),(5,5)))