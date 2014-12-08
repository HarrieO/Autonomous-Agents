import numpy as np 
from world import World
import collections as col
from policies import greedy_policy

def policyHillClimbing(episodes,initial_state,gamma=0.5, delta=0.2, alpha=1.0):
	world = World((5,5),initial_state)
	# initialization might be too expansive
	Q_pred = col.Counter()
	Q_prey = col.Counter()
	seen_states = [] # keep track of seen states 
	pi_pred = col.Counter()
	pi_prey = col.Counter()
	initValue = 1.0
	num_actions_prey = len(world.singleMoveList())
	num_actions_pred = len(world.allMoveList())
	steps = [0]*episodes
	rewards = [0]*episodes
	for i in range(episodes):
		# initialize world
		world = World((5,5),initial_state)
		iterations =0
		state = world.position
		seen_states.append(state)
		for action_p in world.singleMoveList():
			Q_prey[(state, action_p)] = initValue
			pi_prey[(state, action_p)] = initValue/float(num_actions_prey)
		for action_p in world.allMoveList():
			Q_pred[(state,action_p)]=initValue
			pi_pred[(state, action_p)] = initValue/float(num_actions_pred)
		while True:
			# choose action
			action_pred = greedy_policy(pi_pred, state, world.allMoveList())
			action_prey = greedy_policy(pi_prey, state, world.singleMoveList())
			reward = world.move(action_prey,action_pred)
			new_state = world.position
			iterations +=1
			# update Q
			if new_state not in seen_states:
				seen_states.append(new_state)
				for action_p in world.singleMoveList():
					Q_prey[(state, action_p)] = initValue
					pi_prey[(state, action_p)] = initValue/float(num_actions_prey)
				for action_p in world.allMoveList():
					Q_pred[(state,action_p)]=initValue
					pi_pred[(state, action_p)] = initValue/float(num_actions_pred)
			best_Q_pred = max([Q[(new_state,action)] for action in world.allMoveList()])
			best_Q_prey = max([Q[(new_state,action)] for action in world.singleMoveList()])
			Q_pred[(state,action_pred,action_prey)] = (1.0-alpha)*Q_pred[(state,action_pred,action_prey)] + alpha*(reward[1]+ gamma* best_Q_pred)
			Q_prey[(state,action_prey,action_pred)] = (1.0-alpha)*Q_prey[(state,action_prey,action_pred)] + alpha*(reward[0]+ gamma* best_Q_prey)
			# update pi for predator and prey
			if Q_pred[(state,action_pred)] ==  max([Q_pred[(state,action)] for action in world.allMoveList()]):
				pi[(s,a)]+= delta
			else:
				pi[(s,a)]-= delta/(num_actions_pred-1.0)
			if Q_prey[(state,action_prey)] ==  max([Q_prey[(state,action)] for action in world.singleMoveList()]):
				pi[(s,a)]+= delta
			else:
				pi[(s,a)]-= delta/(num_actions_prey-1.0)
			# restrict to probability distribution
			sum_value = sum([Q_pred[(state,action)] for action in world.allMoveList()])
			pi_pred /= sum_value
			sum_value = sum([Q_prey[(state,action)] for action in world.singleMoveList()])
			pi_prey /= sum_value

			#alpha *= decay
			# check terminal state
			if reward[0]!=0:
				rewards[i]=reward[0]
				steps[i]= iterations
				break
			state = new_state
	return steps, rewards

predatorLocations = [(0,0)]

episodes = 10000
steps, rewards = policyHillClimbing(episodes, predatorLocations)
