from world import World 
import random
import numpy as np

# returns list of indices with max values of list
def maxIndices(valueActionList):
	maxv    = None
	indices = []
	for i, (value, action) in enumerate(valueActionList):
		if not maxv or value > maxv:
			indices = [i]
			maxv = value
		elif value == maxv:
			indices.append(i)
	return indices

# picks an action according to epsilon-greedy policy
def epsGreedyPolicy(state, world, Q, epsilon):
	valuePerAction = [(Q[state,move], move) for move in world.moveList()]

	probs = [epsilon/len(valuePerAction)]*len(valuePerAction)
	maxInd = maxIndices(valuePerAction)
	for i in maxInd:
		probs[i] += (1-epsilon)/len(maxInd)

	# picks an action,value pair over given probability distribution
	_,action = world.pickElementWithProbs(zip(valuePerAction,probs))
	
	return action

def MCon(episodes, initValue=0.0,epsilon=0.1, alpha=0.5,discount=0.1):
	# world object, (starting state is trivial)
	world = World((0,0),(1,1))

	# initialize Q value table and Return list for every (s,a)-pair
	Q = {}
	R = {}
	for state in world.allStates():
		for move in world.moveList():
			Q[state,move] = initValue # some value
			R[state,move] = [] # empty list; return = cummulative discounted reward
	steps = [0]*episodes # list counting number of iterations

	for i in range(episodes):
		iterations = 0
		# initialize world
		world.setState((-5,-5))
		stateActionPairs = {}
		# generate an episode using current policy
		while True:
			state = world.position
			# move the predator according to policy
			action = epsGreedyPolicy(state, world, Q, epsilon)
			world.move(action)
			if not (state,action) in stateActionPairs: # store first occurence
				stateActionPairs[(state,action)] = iterations # will be used for discounting
			iterations += 1
			# check if predator caught the prey
			if world.stopState():
				break
			# move the prey (stochasticly)
			world.performPreyMove()
			newState = world.position
		steps[i] = iterations # save amount of iterations needed to catch the prey
		# update Q and R
		for pair in stateActionPairs.keys():
			firstReturn = 10.0*discount**stateActionPairs[pair] # always zero but 10 when episode ends
			R[pair].append(firstReturn)
			Q[pair] = np.mean(np.array(R[pair]))
		# update policy done in epsilon greedy policy code
	return steps