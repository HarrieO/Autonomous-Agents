import numpy as np 
from world import World
import collections as col
from policies import greedy_policy

def policyHillClimbing(episodes,initial_state,gamma=0.5, delta=0.2, alpha_pred=0.4, alpha_prey=0.1):
	world = World((5,5),initial_state)
	# initialization might be too expansive
	Q_pred = {}
	Q_prey = {}
	seen_states = [] # keep track of seen states 
	pi_pred = {}
	pi_prey = {}
	initValue = 0.0
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
		seen_states.append((0,0))
		for action_p in world.singleMoveList():
			Q_prey[(state, action_p)]  = initValue
			pi_prey[(state, action_p)] = 1/float(num_actions_prey)
			Q_prey[((0,0), action_p)]  = 0
		for action_p in world.allMoveList():
			Q_pred[(state,action_p)]   = initValue
			pi_pred[(state, action_p)] = 1/float(num_actions_pred)
			Q_pred[((0,0), action_p)]  = 0
		while not world.stopState():
			state = world.position
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
					Q_prey[(new_state, action_p)]  = initValue
					pi_prey[(new_state, action_p)] = 1/float(num_actions_prey)
				for action_p in world.allMoveList():
					Q_pred[(new_state,action_p)]   = initValue
					pi_pred[(new_state, action_p)] = 1/float(num_actions_pred)

			best_Q_pred = max([Q_pred[(new_state,action)] for action in world.allMoveList()])
			best_Q_prey = max([Q_prey[(new_state,action)] for action in world.singleMoveList()])
			Q_pred[(state,action_pred)] = (1.0-alpha_pred)*Q_pred[(state,action_pred)] + alpha_pred*(reward[1]+ gamma* best_Q_pred)
			Q_prey[(state,action_prey)] = (1.0-alpha_prey)*Q_prey[(state,action_prey)] + alpha_prey*(reward[0]+ gamma* best_Q_prey)
			# update pi for predator and prey
			if Q_pred[(state,action_pred)] ==  max([Q_pred[(state,action)] for action in world.allMoveList()]):
				pi_pred[(state,action_pred)] += delta
			else:
				pi_pred[(state,action_pred)] -= delta/(num_actions_pred-1.0)
			if Q_prey[(state,action_prey)] ==  max([Q_prey[(state,action)] for action in world.singleMoveList()]):
				pi_prey[(state,action_prey)] += delta
			else:
				pi_prey[(state,action_prey)] -= delta/(num_actions_prey-1.0)

			# restrict to probability distribution and make it epsilon greedy (divide 0.1 over all actions)
			sum_value = sum([Q_pred[(state,action)] for action in world.allMoveList()])
			for action_p in world.allMoveList():
				if sum_value > 0:
					pi_pred[(state, action_p)] /= sum_value
				pi_pred[(state, action_p)] *= 0.9
				pi_pred[(state, action_p)] += 0.1/num_actions_pred
			sum_value = sum([Q_prey[(state,action)] for action in world.singleMoveList()])
			for action_p in world.singleMoveList():
				if sum_value > 0:
					pi_prey[(state, action_p)] /= sum_value
				pi_prey[(state, action_p)] *= 0.9
				pi_prey[(state, action_p)] += 0.1/num_actions_prey

			#alpha *= decay

		rewards[i]=reward[0]
		steps[i]= iterations
		print "Episode", i
	return steps, rewards

