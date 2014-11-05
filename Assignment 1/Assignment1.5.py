from world    import World
from prey     import Prey
from agent 	  import Agent
import numpy as np
import time


# Returns the minimal distance the predator needs to reach the preyloc
# Considering that world is repeated
def mindistance(x1, x2):
	return ((x1-x2)+5)%11-5

# given absolute positions the relative position is returned
def rewriteStates(predloc, preyloc):
	return (mindistance(predloc[0],preyloc[0]),mindistance(predloc[1],preyloc[1]))


def valueIteration():

	alldiffs = [ (x,y) for x in range(-5,6) for y in range(-5,6)]
	alldiffs.remove((0,0))

	# the relative positions vary from -5 up to 5, in both dimensions
	values = {}
	for x in range(-5,6):
		for y in range(-5,6):
			values[(x,y)] = 0

	bestMoves = {}
	agent = Agent(0,0)

	deltas = []
	discountFactor = 0.8
	epsilon = 0.01
	delta = 1
	while delta > epsilon:
		delta = 0
		newValues = {}
		for diff in alldiffs:
			# we place the predator in the middle of the world,
			# we are allowed to do this, since the positions are encoded relatively
			predloc = (5,5)
			preyloc = (predloc[0]+diff[0],predloc[1]+diff[1])
			curKey  = rewriteStates(predloc,preyloc)
			agent.setLocation(predloc)
			prey = Prey(*preyloc)
			temp = values[curKey]
			bestVal = 0
			bestMove = (0,0)
			for prob, predMove in agent.getMoveList():
				preySum = 0
				newPredloc = agent.locAfterMove(predMove)
				if newPredloc == preyloc :
					preySum += 10.0
				else:
					for preyProb, newPreyloc in prey.expand(newPredloc):
						# using rewriteStates we use relative positions
						preySum += preyProb * discountFactor * values[rewriteStates(newPredloc,newPreyloc)]
				if bestVal <= preySum:
					bestVal = preySum
					bestMove = predMove
			newValues[curKey] = bestVal
			bestMoves[curKey] = bestMove
			delta = max(delta, np.abs(bestVal - temp))
		values = newValues
		deltas.append(delta)

	def policy(state):
		predloc, preyloc = state
		agent.setLocation(predloc)
		prey = Prey(*preyloc)
		return bestMoves[rewriteStates(predloc,preyloc)]
	return policy

start = time.time()
policy = valueIteration()
print "Time taken", round((time.time()-start)*10000)/100, "seconds"
print policy(((0,1),(0,2)))
print policy(((0,2),(0,0)))
print policy(((0,0),(5,5)))