from world import World 
import random
import numpy as np
from Qlearning import Qlearning
from policies import softmaxPolicy, epsGreedyPolicy, maxIndices
from pylab import *

runCount = 100
epiCount = 600

class OptimalCheck(object):
	# we perform value iteration to determine which actions are optimal
	def __init__(self, policy):
		# world object, (starting state is trivial)
		world = World((0,0),(1,1))
		value = {}
		for state in world.allStates():
			value[state] = 0
		discount = 0.9
		delta = 1
		while abs(delta) > 0.00001:
			delta = 0
			for state in world.allStates():
				world.setState(state)
				old = value[state]
				# we can set the minimum to 0 since we know every value will be 0 or positive
				curMax = 0
				for move in world.moveList():
					if world.posAfterMove(move) == (0,0):
						probSum = 10
					else:
						probSum = 0
						for nextState,prob in world.nextPreyStates():
							probSum += prob*discount*value[nextState]
					curMax = max(curMax,probSum)
				value[state] = curMax
				delta = max(delta,abs(old - curMax))
		value[(0,0)] = 10
		self.value 		  = value
		self.actionList   = []
		self.allList  = []
		self.bottomPolicy = policy
		self.discount     = discount

	def isOptimal(self,state, move):
		world    = World((0,0),(1,1))
		ourMove  = 0
		bestMove = 0
		for nmove in world.moveList():
			world.setState(state)
			world.move(nmove)
			if world.position == (0,0):
				probSum = 10
			else:
				probSum = 0
				for nextState,prob in world.nextPreyStates():
					probSum += prob*self.discount*self.value[nextState]
			bestMove = max(bestMove,probSum)
			if nmove == move:
				ourMove = probSum
		return ourMove/bestMove > 0.97
	
	def policy(self,state,world, Q, policyParam):
		action = self.bottomPolicy(state,world,Q,policyParam)
		if self.isOptimal(state,action):
			self.actionList += [1]
		else:
			self.actionList += [0]
		if world.posAfterMove(action) == (0,0):
			self.allList.append(self.actionList)
			self.actionList = []
		return action


figure()
ylim(0,100)
labels =[]
optimList = []
for di, temperature in enumerate([0.1,0.5,0.9]):
	
	steps = np.zeros((runCount,epiCount))
	optim = np.zeros((runCount,epiCount))
	for i in range(runCount):
		oc = OptimalCheck(softmaxPolicy)
		steps[i,:] = np.array(Qlearning(epiCount,oc.policy,policyParam=temperature,initValue=5))
		optim[i,:] = np.array([ sum(actlist)/float(len(actlist)) for actlist in oc.allList])
		
	aveSteps = np.mean(steps, axis=0)
	aveOptimal = np.mean(optim, axis=0)

	optimList.append(aveOptimal)

	t = range(1, aveSteps.shape[0]+1)
	labels += [r"$\tau = " +str(temperature)+ "$"]
	plot(t, aveSteps)
	draw()

for di, epsilon in enumerate([0.1,0.3,0.5]):
	
	steps = np.zeros((runCount,epiCount))
	optim = np.zeros((runCount,epiCount))
	for i in range(runCount):
		oc = OptimalCheck(epsGreedyPolicy)
		steps[i,:] = np.array(Qlearning(epiCount,oc.policy,policyParam=epsilon,initValue=5))
		optim[i,:] = np.array([ sum(actlist)/float(len(actlist)) for actlist in oc.allList])
	
	aveSteps = np.mean(steps, axis=0)
	aveOptimal = np.mean(optim, axis=0)

	optimList.append(aveOptimal)

	t = range(1, aveSteps.shape[0]+1)
	labels += [r"$\epsilon = " +str(epsilon)+ "$"]
	plot(t, aveSteps)
	draw()




plt.legend(labels)
xlabel('episodes')
ylabel('Average steps per episode')
title(r'Average steps per episode with Q-learning with softmax-policy.')
grid(True)
savefig("plots/steps2.3.1.png")
xlim(0,100)
savefig("plots/steps2.3.2.png")
close()

figure()
t = range(1, optim.shape[1]+1)
for i in range(len(optimList)):
	plot(t, optimList[i])

ylim(0,1)
plt.legend(labels, loc='lower right')
xlabel('episodes')
ylabel('Percentage of optimal action taken')
title(r'Percentage of optimal actions taken per episode with Q-learning.')
grid(True)
savefig("plots/opt2.3.png")
close()
