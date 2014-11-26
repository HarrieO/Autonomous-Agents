from world import World 
from policies import epsGreedyPolicy, maxIndices
import numpy as np
import random

def MCoff(episodes, behaPolicy=None, initValue=15,discount=0.9):
	# behaPolicy = dictionary with keys (state,action) and value P(action|state)

	world = World((0,0),(1,1))

	movelist = world.moveList()
	behaPolicy = {}
	for state in world.allStates():
		for move in movelist:
			behaPolicy[(state, move)] = 1.0/len(movelist)
	def policy(world):
		return world.pickElementWithProbs([(move,behaPolicy[(world.position,move)]) for move in movelist])

	ourPolicy = {}
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
			ourPolicy[state] = move
	steps = [0]*episodes # list counting number of iterations

	for epi in range(episodes):
		time = 0
		totalTime =0
		# initialize world
		world.setState((-5,-5))
		
		episode = []
		while True:
			action = policy(world)
			episode.append((world.position, action))
			world.move(action)
			if world.stopState():
				break
			else:
				world.performPreyMove()

		# save the pairs that match, and their first occurence
		matchingHistory = {}
		# last time move was equal to policy
		last = 0
		for i, (state, action) in enumerate(episode[::-1]):
			actionValues = [(maction, Q[state,maction]) for maction in world.moveList()]
			bestActions = [actionValues[j][0] for j in maxIndices(actionValues)]
			if action not in bestActions:
				last = len(episode)-i
				break
			matchingHistory[(state, action)] = len(episode)-i - 1

		for (state, action) in matchingHistory:
			w = np.prod([ 1.0/behaPolicy[episode[j]] for j in range(matchingHistory[(state, action)],len(episode))])
			num[(state,move)]  +=  w* (10.0*discount**matchingHistory[(state, action)]) # return is gamma^{T-t}*10
			denum[(state,move)]+= w
			Q[(state,move)]= num[(state,move)]/float(denum[(state,move)])

		iterations = 0
		while True:
			iterations += 1
			actionValues = [(maction, Q[state,maction]) for maction in world.moveList()]
			bestAction = random.choice([actionValues[j][0] for j in maxIndices(actionValues)])
			world.move(bestAction)
			if world.stopState():
				break
			else:
				world.performPreyMove()
		steps[epi] = iterations
		
			
	return steps
