from world import World
import pylab as plt

def Qlearning(episodes, initialState,policy):

    alpha = 0.3
    initValue=5
    policyParam=0.1
    alpha=0.4
    discount=0.9
    # world object, (starting state is trivial)
    world = World((5,5),initialState)

    # Q value table
    Q_pred = {}
    Q_prey = {}


    steps = [0]*episodes
    rewards = [0]*episodes
    for i in range(episodes):
        iterations = 0
        # initialize world
        world = World((5,5),initialState)
        while True:
            state = world.position
            # move the predator according to policy with one parameter (epsilon for E-greedy or Tua for softmax)
            pred_action = policy(state, world.allMoveList(),    Q_pred, policyParam, initValue)
            prey_action = policy(state, world.singleMoveList(), Q_prey, policyParam, initValue)
            reward      = world.move(prey_action, pred_action)
            iterations += 1

            if (state,prey_action) not in Q_prey:
                Q_prey[state,prey_action] = initValue
            if (state,pred_action) not in Q_pred:
                Q_pred[state,pred_action] = initValue

            # check if predator caught the prey
            if world.stopState():
                # the Q(s,a) update rule (note that the next state is the absorbing state)
                Q_prey[state,prey_action] = Q_prey[state,prey_action] + alpha * (reward[0] - Q_prey[state,prey_action])
                Q_pred[state,pred_action] = Q_pred[state,pred_action] + alpha * (reward[1] - Q_pred[state,pred_action])
                break
            # move the prey (stochasticly)
            newState = world.position
            # the maximum value the agent can have after another move
            maxQ_pred = max([Q_pred.get((newState,nextAction),initValue) for nextAction in world.allMoveList()])
            maxQ_prey = max([Q_prey.get((newState,nextAction),initValue) for nextAction in world.singleMoveList()])
            # the Q(s,a) update rule (note that the immediate reward is zero)
            Q_pred[state,pred_action] = Q_pred[state,pred_action] + alpha * ( discount*maxQ_pred - Q_pred[state,pred_action])
            Q_prey[state,prey_action] = Q_prey[state,prey_action] + alpha * ( discount*maxQ_prey - Q_prey[state,prey_action])
        # print the number of steps the predator took
        steps[i]   = iterations
        if reward[1] > 0:
            rewards[i] = 1

    return steps, rewards