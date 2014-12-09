import numpy as np 
import world
import policies
from cvxopt import matrix, solvers

def minimax(episodes,initial_state,epsilon, decay, gamma, alpha=1.0):
    # initialization might be too expansive
    Q_pred = dict()
    Q_prey = dict()
    V_pred = dict()
    V_prey = dict()
    pi_pred = dict()
    pi_prey = dict()
    initValue = 1.0
    # for state in states:
    #   V_pred[state] = 1.0
    #   V_prey[state] = 1.0
    #   for action in predator_moves:
    #       pi_pred[(state,action)]=1.0/num_actions
    #       for opponent_move in opponent_moves:
    #           Q_pred[(state,action, prey_move)]=1.0
    #           Q_prey[(state,opponent_move,action)]=1.0
    #   for action in prey_move:
    #       pi_pred[(state,action)]=1.0/num_actions
    steps = [0]*episodes
    rewards = [0]*episodes
    for i in range(episodes):
        # initialize world
        world = World((5,5),initialState)
        # maxQ[s] stores the action that maximises Q(s,a)
        maxQ_prey = {}
        maxQ_pred = {}
        iterations =0
        while True:
            state = world.position
            # choose action
            action_pred = minimax_policy(epsilon, pi_pred, state, world.allMoveList())
            action_prey = minimax_policy(epsilon, pi_prey, state, world.singleMoveList())
            reward = world.move(action_prey,action_pred)
            iterations +=1
            # update Q
            if (state,action_prey) not in Q_prey:
                Q_prey[state,action_prey] = initValue
            if (state,action_pred) not in Q_pred:
                Q_pred[state,action_pred] = initValue
            Q_pred[(state,action_pred,action_prey)] = (1.0-alpha)*Q_pred[(state,action_pred,action_prey)] + alpha*(reward[1]+ gamma* V_pred[new_state])
            Q_prey[(state,action_prey,action_pred)] = (1.0-alpha)*Q_prey[(state,action_prey,action_pred)] + alpha*(reward[0]+ gamma* V_prey[new_state])

            # update pi

            # update V
            #[pi_pred[(s,action_pd)]*Q[s,action_pd, action_py]]
            alpha *= decay
            # check terminal state
            if reward[0]!=0:
                rewards[i]=reward[0]
                steps[i]= iterations
                break
