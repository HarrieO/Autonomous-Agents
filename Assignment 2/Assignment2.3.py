from Assignment21 import *
from world import World 
import random
import numpy as np

# picks an action according to the softmax policy
def softmaxPolicy(state, world, Q, tau):
	valuePerAction = np.array([np.exp(Q[state,move]/float(tau)) for move in world.moveList()])
	totalSum = np.sum(valuePerAction)
	probs = valuePerAction/totalSum 
	# picks an action,value pair over given probability distribution
	return world.pickElementWithProbs(zip(world.moveList(),probs))

print Qlearning(10)
