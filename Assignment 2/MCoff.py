from world import World 
from policies import epsGreedyPolicy, maxIndices
import numpy as np
import random

def MCoff(episodes, behaPolicy, matches=[], initValue=15,discount=0.9):
	# behaPolicy = dictionary with keys (state,action) and value P(action|state)


	world = World((0,0),(1,1))
	movelist = world.moveList()
	def policy(world):
		return world.pickElementWithProbs([(move,behaPolicy[(world.position,move)]) for move in movelist])

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
	for epi in range(episodes):
		time = 0
		totalTime =0
		# initialize world
		world.setState((-5,-5))
		
		episode = []
		while True:
			action = policy(world)
			episode.append((world.position, action))
			if action == None:
				print action, state
			world.move(action)
			if world.stopState():
				break
			world.performPreyMove()

		# save the pairs that match, and their first occurence
		matchingHistory = {}
		# last time move was equal to policy
		last = 0
		for i, (state, action) in enumerate(episode[::-1]):
			actionValues = [(Q[state,maction],maction) for maction in world.moveList()]
			bestActions = [actionValues[j][1] for j in maxIndices(actionValues)]
			matchingHistory[(state, action)] = len(episode)-i - 1
			if action not in bestActions:
				last = len(episode)-i
				break
			
		
		matches.append(len(episode)-last)
		
		for (state, action) in matchingHistory:
			if matchingHistory[(state, action)] >= last-1:
				w = np.prod([ 1.0/behaPolicy[episode[j]] for j in range(matchingHistory[(state, action)],len(episode))])
				num[(state,move)]   += w * (10.0*discount**matchingHistory[(state, action)]) # return is gamma^{T-t}*10
				denum[(state,move)] += w
				Q[(state,move)]= num[(state,move)]/float(denum[(state,move)])

		world.setState((-5,-5))
		iterations = 0
		while True:
			iterations += 1
			actionValues = [(maction, Q[state,maction]) for maction in world.moveList()]
			bestAction = random.choice([actionValues[j][0] for j in maxIndices(actionValues)])
			world.move(bestAction)
			if world.stopState() or iterations > 2000:
				break
			world.performPreyMove()
		steps[epi] = iterations
		
			
	return steps
