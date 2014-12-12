import numpy as np
import random

def pickElementWithProbs(elemProbList):
	pick = random.random()
	for elem, prob in elemProbList:
		if pick <= prob:
			return elem
		pick -= prob
	return elemProbList[-1][0]

# returns list of indices with max values of list
def maxIndices(valueActionList):
	maxv    = None
	indices = []
	for i, (value, action) in enumerate(valueActionList):
		if maxv == None or value > maxv:
			indices = [i]
			maxv = value
		elif value == maxv:
			indices.append(i)
	return indices

# picks an action according to epsilon-greedy policy
def epsGreedyPolicy(state, moveList, Q, epsilon, initValue):
	valuePerAction = [(Q.get((state,move),initValue), move) for move in moveList]
	probs = [epsilon/len(valuePerAction)]*len(valuePerAction)
	maxInd = maxIndices(valuePerAction)
	for i in maxInd:
		probs[i] += (1-epsilon)/len(maxInd)
	# picks an action,value pair over given probability distribution
	_,action = pickElementWithProbs(zip(valuePerAction,probs))
	return action

# picks an action according to the softmax policy
def softmaxPolicy(state, moveList, Q, tau):
	valuePerAction = np.array([np.exp(Q[state,move]/float(tau)) for move in moveList])
	totalSum = np.sum(valuePerAction)
	probs = valuePerAction/totalSum 
	# picks an action,value pair over given probability distribution
	return pickElementWithProbs(zip(world.moveList(),probs))

# hybrid between softmax and epsilon-greedy
def minimax_policy(epsilon,values, state, actions):
	if random.random() < epsilon:
		return random.choice(actions)
	probabilities = [values[(state,action)] for action in actions]
	totalSum = np.sum(probabilities)
	probs = probabilities/totalSum
	# picks an action,value pair over given probability distribution
	return pickElementWithProbs(zip(actions,probs))

# selects action according to given probabilities
def greedy_policy(values, state, actions):
	probabilities = [(action,values[(state,action)]) for action in actions]
	totalSum = np.sum(probabilities)
	probs = probabilities/totalSum
	# picks an action,value pair over given probability distribution
	return pickElementWithProbs(zip(actions,probs))
