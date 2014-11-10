from world import World 
import random

# world object, (starting state is trivial)
world = World((0,0),(1,1))

# pick all starting states in random order
startingStates = world.allStates()
random.shuffle(startingStates)

# epsilon used for epsilon greedy
epsilon  = 0.1
alpha    = 0.5
discount = 0.3
# Q value table
Q = {}
for state in startingStates:
	for move in world.moveList():
		Q[state,move] = 15

# returns list of indices with max values of list
def maxIndices(valueActionList):
	maxv    = None
	indices = []
	for i, (value, action) in enumerate(valueActionList):
		if value == maxv:
			indices.append(i)
		elif value > maxv:
			indices = [i]
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


for i in range(500):
	iterations = 0
	world.setState(random.choice(startingStates))
	while True:
		state = world.position
		action = epsGreedyPolicy(state, world, Q, epsilon)

		world.move(action)
		if world.stopState():
			Q[state,action] = Q[state,action] + alpha * (10 - Q[state,action])
			print iterations
			break

		world.performPreyMove()
		newState = world.position
		iterations += 1

		maxQ = max([Q[(newState,action)] for action in world.moveList()])
		Q[(state,action)] = Q[state,action] + alpha * ( discount*maxQ - Q[state,action])

