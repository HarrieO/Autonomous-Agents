import numpy as np 
from world import World
from policies import *
from cvxopt import matrix, solvers

solvers.options['show_progress'] = False

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
    world = World((5,5),initial_state)
    for state in world.allStates():
      V_pred[state] = 1.0
      V_prey[state] = 1.0
      for action in world.allMoveList():
          pi_pred[(state,action)]=1.0/len(world.allMoveList())
          for prey_move in world.singleMoveList():
              Q_pred[(state, action, prey_move)]=1.0
              Q_prey[(state, action, prey_move)]=1.0
      for action in world.singleMoveList():
          pi_prey[(state,action)]=1.0/len(world.singleMoveList())
    # absorbing states
    terminal_state = tuple([(0,0)] * len(initial_state))
    V_pred[terminal_state] = 0.0
    V_prey[terminal_state] = 0.0

    steps = [0]*episodes
    rewards = [0]*episodes
    for epi in range(episodes):
        
        # initialize world
        world = World((5,5),initial_state)

        # print "Begin Pred", V_pred[world.position]
        # print "End   Prey", V_prey[world.position]
        # for s in world.singleMoveList():
        #     print s, "Pred", V_pred[(s,)]
        #     print s, "Prey", V_pred[(s,)]
        #     for a in world.allMoveList():
        #         for a2 in world.singleMoveList():
        #             print s, "Q", a, a2, Q_pred[(state,a,a2)]

        iterations =0
        while not world.stopState():
            state = world.position
            # choose action
            action_pred = minimax_policy(epsilon, pi_pred, state, world.allMoveList())
            action_prey = minimax_policy(epsilon, pi_prey, state, world.singleMoveList())
            
            reward = world.move(action_prey,action_pred)
            iterations +=1
            new_state = world.position

            # update Q
            # if (state,action_prey) not in Q_prey:
            #     Q_prey[state,action_prey] = initValue
            # if (state,action_pred) not in Q_pred:
            #     Q_pred[state,action_pred] = initValue 
            Q_pred[(state,action_pred,action_prey)] = (1.0-alpha)*Q_pred[(state,action_pred,action_prey)] + alpha*(reward[1]+ gamma* V_pred[new_state])
            # Q_prey[(state,action_pred,action_prey)] = (1.0-alpha)*Q_prey[(state,action_pred,action_prey)] + alpha*(reward[0]+ gamma* V_prey[new_state])

            # update pi
            # adapted from example: http://abel.ee.ucla.edu/cvxopt/examples/tutorial/lp.html

            ##  PREDATOR update
            # constraint to minimize w.r.t. prey action
            minConstr   = [[1.0] + [-Q_pred[(state,a_pred,a_prey)] for a_pred in world.allMoveList()] for a_prey in world.singleMoveList()]
            # constrinat to keep every pi(a) positive
            posConstr   = []
            for i in range(1,len(world.allMoveList())+1):
                new_row    = [0.0] * (len(world.allMoveList())+1)
                new_row[i] = -1.0
                posConstr.append(new_row)

            normGreater = [0.0] + [1.0] * len(world.allMoveList())
            normSmaller = [0.0] + [-1.0] * len(world.allMoveList())

            A = matrix([normGreater, normSmaller] + minConstr + posConstr).trans()
            b = matrix([ 1.0, -1.0] + [0.0] * (len(world.singleMoveList()) + len(world.allMoveList())) )
            # -1 V and 0 for all pi(s,a)
            c = matrix([ -1.0 ] + [0.0] * len(world.allMoveList()))

            sol=solvers.lp(c,A,b)

            V_pred[state] = sol['x'][0]
            for a_pred, x in zip(world.allMoveList(),sol['x'][1:]):
                pi_pred[(state,a_pred)] = x

            # ## PREY update
            # constraint to minimize w.r.t. prey action
            minConstr   = [[1.0] + [-Q_prey[(state,a_pred,a_prey)] for a_prey in world.singleMoveList()] for a_pred in world.allMoveList()]
            # # constriant to keep every pi(a) positive
            posConstr   = []
            for i in range(1,len(world.singleMoveList())+1):
                new_row    = [0.0] * (len(world.singleMoveList())+1)
                new_row[i] = -1.0
                posConstr.append(new_row)

            normGreater = [0.0] + [ 1.0] * len(world.singleMoveList())
            normSmaller = [0.0] + [-1.0] * len(world.singleMoveList())

            A = matrix([normGreater, normSmaller] + minConstr + posConstr).trans()
            b = matrix([ 1.0, -1.0] + [0.0] * (len(world.allMoveList()) + len(world.singleMoveList())) )
            # -1 V and 0 for all pi(s,a)
            c = matrix([ -1.0 ] + [0.0] * len(world.singleMoveList()))

            sol=solvers.lp(c,A,b)
        
            V_prey[state] = sol['x'][0]
            for a_prey, x in zip(world.singleMoveList(),sol['x'][1:]):
                pi_prey[(state,a_prey)] = x


            alpha *= decay
        print "Episode",epi
        steps[epi]   = iterations
        if reward[1] > 0:
            rewards[epi] = 1
    return steps, rewards
