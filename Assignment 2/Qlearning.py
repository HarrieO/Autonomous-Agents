from world import World 

def Qlearning(episodes, policy, initValue=15,policyParam=0.1, alpha=0.4,discount=0.9):
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
			# move the predator according to policy with one parameter (epsilon for E-greedy or Tua for softmax)
			action = policy(state, world, Q, policyParam)
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