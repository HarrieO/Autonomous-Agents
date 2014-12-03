import numpy as np

# returns list of indices with max values of list
def maxIndices(valueActionList):
	maxv    = None
	indices = []
	for i, (value, action) in enumerate(valueActionList):
		if (not maxv) or value > maxv:
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

# picks an action according to the softmax policy
def softmaxPolicy(state, world, Q, tau):
	valuePerAction = np.array([np.exp(Q[state,move]/float(tau)) for move in world.moveList()])
	totalSum = np.sum(valuePerAction)
	probs = valuePerAction/totalSum 
	# picks an action,value pair over given probability distribution
	return world.pickElementWithProbs(zip(world.moveList(),probs))