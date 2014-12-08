import numpy as np 

def minimax_policy(epsilon,values, state):
	probabilities = [epsilon+(1.0-epsilon)*values[(state,action)] for action in actions]
	return action_according_to_probabilities

def minimax(num_its,epsilon, decay, gamma):
	# initialize
	Q_pred = dict()
	Q_prey = dict()
	V_pred = dict()
	V_prey = dict()
	pi_pred = dict()
	pi_prey = dict()
	for state in states:
		V_pred[state] = 1.0
		V_prey[state] = 1.0
		for action in predator_moves:
			pi_pred[(state,action)]=1.0/num_actions
			for opponent_move in opponent_moves:
				Q_pred[(state,action, prey_move)]=1.0
				Q_prey[(state,opponent_move,action)]=1.0
		for action in prey_move:
			pi_pred[(state,action)]=1.0/num_actions
	alpha = 1.0
	# initialize world

	for i in range(num_its):
		# choose action
		action_pred = minimax_policy(epsilon, pi_pred, state)
		action_prey = minimax_policy(epsilon, pi_prey, state)
		# check terminal state

		# update Q
		Q_pred[(state,action_pred,action_prey)] = (1.0-alpha)*Q_pred[(state,action_pred,action_prey)] + alpha*gamma* V_pred[new_state]
		Q_prey[(state,action_prey,action_pred)] = (1.0-alpha)*Q_prey[(state,action_prey,action_pred)] + alpha*gamma* V_prey[new_state]
		# update pi
		# update V
		[pi_pred[(s,action_pd)]*Q[s,action_pd, action_py]]
		alpha *= decay
