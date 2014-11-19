from world import World 
from policies import epsGreedyPolicy, maxIndices

def MCoff(episodes, behaviorPolicy, policyProb,initValue=0.0,epsilon=0.1, alpha=0.5,discount=0.1):
	# policyProb = dictionary with keys (state,action) and value P(action|state)

	# world object, (starting state is trivial)
	world = World((0,0),(1,1))

	# initialize Q value table and Return list for every (s,a)-pair
	Q = {}
	R = {}
	num = {}
	denum = {} 
	for state in world.allStates():
		for move in world.moveList():
			num[state,move] = 0.0
			denum[state,move] = 0.0
			Q[state,move] = float(initValue) # some value
			R[state,move] = [] # empty list; return = cummulative discounted reward
	steps = [0]*episodes # list counting number of iterations

	for i in range(episodes):
		time = 0
		totalTime =0
		# initialize world
		world.setState((-5,-5))
		stateActionPairs = {}
		# generate an episode using fixed policy
		history = {} # save history
		historyAll = [] # all history from tau forwards
		while True:
			state = world.position
			# move the predator according to policy
			action = behaviorPolicy(state, world, Qinit, epsilon)
			world.move(action)
			actionValues = [(maction, Q(state,maction)) for maction in world.moveList()]
			bestAction = actionValues[maxIndices(actionValues)[0]][0]
			if action != bestAction:
				history = {} # forget history
				historyAll = []
			historyAll.append((state,action))
			if not (state,action) in history: # store first occurence
				history[(state,action)] = totalTime # will be used for discounting
			# check if predator caught the prey
			if world.stopState():
				break
			# move the prey (stochasticly)
			world.performPreyMove()
			newState = world.position
			totalTime+=1
		steps[i] = totalTime # save amount of iterations needed to catch the prey
		# compute mu's 
		mu = np.zeros(len(historyAll))
		for t in range(len(historyAll)):
			mu[t]=policyProb[historyAll[t]]
		mu = 1.0/mu
		# update Q,N,D
		for (state,move) in history.keys():
			t = history[(state,move)] # first occurence time 
			W = np.prod(1.0/mu[t-totalTime:])
			num[(state,move)]+= float(W* (10.0*discount**(totalTime-time))) # return is gamma^{T-t}*10
			denum[(state,move)]+= float(W)
			Q[(state,move)]= float(W*Gt)/float(W)
	return steps
