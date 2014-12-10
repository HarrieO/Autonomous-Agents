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
    # initialisation
    world = World((5,5),initialState)
    for state in world.allStates():
      V_pred[state] = 1.0
      V_prey[state] = 1.0
      for action in world.allMoveList():
          pi_pred[(state,action)]=1.0/num_actions
          for opponent_move in opponent_moves:
              Q_pred[(state,action, prey_move)]=1.0
              Q_prey[(state,opponent_move,action)]=1.0
      for action in world.singleMoveList():
          pi_pred[(state,action)]=1.0/num_actions

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
            # if (state,action_prey) not in Q_prey:
            #     Q_prey[state,action_prey] = initValue
            # if (state,action_pred) not in Q_pred:
            #     Q_pred[state,action_pred] = initValue
            Q_pred[(state,action_pred,action_prey)] = (1.0-alpha)*Q_pred[(state,action_pred,action_prey)] + alpha*(reward[1]+ gamma* V_pred[new_state])
            Q_prey[(state,action_prey,action_pred)] = (1.0-alpha)*Q_prey[(state,action_prey,action_pred)] + alpha*(reward[0]+ gamma* V_prey[new_state])

            # update pi
            # adapted from example: http://abel.ee.ucla.edu/cvxopt/examples/tutorial/lp.html

            # constraint to minimize w.r.t. prey action
            minConstr   = [[1.0] + [Q_pred[(state,a_pred,a_prey)] for a_pred in world.allMoveList()] for a_prey in world.singleMoveList()]
            # constrinat to keep every pi(a) positive
            posConstr   = []
            for i in range(1,len(world.allMoveList())+1):
                new_row    = [0.0] * (len(world.allMoveList())+1)
                new_row[i] = -1.0
                posConstr.append(new_row)

            normGreater = [0.0] + [1.0] * len(world.allMoveList())
            normSmaller = [0.0] + [-1.0] * len(world.allMoveList())


            A = matrix([normGreater, normSmaller] + minConstr + posConstr).trans()
            b = matrix([ 1.0, -1.0] + [0.0] * (len(world.singleMoveList()) * 2) )
            # -1 V and 0 for all pi(s,a)
            c = matrix([ -1.0 ] + [0.0] * len(world.allMoveList()))
            sol=solvers.lp(c,A,b)
            print sol
            exit()

            # update V
            #[pi_pred[(s,action_pd)]*Q[s,action_pd, action_py]]
            alpha *= decay
            # check terminal state
            if reward[0]!=0:
                rewards[i]=reward[0]
                steps[i]= iterations
                break
