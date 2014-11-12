from world import World 
import random
import numpy as np
from pylab import *

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

def Qlearning(episodes, policy, initValue=15,epsilon=0.1, alpha=0.5,discount=0.1):
	# world object, (starting state is trivial)
	world = World((0,0),(1,1))

	# Q value table
	Q = {}
	for state in world.allStates():
		for move in world.moveList():
			Q[state,move] = initValue

	steps = [0]*episodes

	for i in range(episodes):
		iterations = 0
		# initialize world
		world.setState((-5,-5))
		while True:
			state = world.position
			# move the predator according to epsilon greedy policy
			action = policy(state, world, Q, epsilon)
			world.move(action)
			iterations += 1
			# check if predator caught the prey
			if world.stopState():
				# the Q(s,a) update rule (note that the next state is the absorbing state)
				Q[state,action] = Q[state,action] + alpha * (10 - Q[state,action])
				break
			# move the prey (stochasticly)
			world.performPreyMove()
			newState = world.position
			# the maximum value the agent can have after another move
			maxQ = max([Q[newState,nextAction] for nextAction in world.moveList()])
			# the Q(s,a) update rule (note that the immediate reward is zero)
			Q[state,action] = Q[state,action] + alpha * ( discount*maxQ - Q[state,action])
		# print the number of steps the predator took
		steps[i] = iterations
	return steps