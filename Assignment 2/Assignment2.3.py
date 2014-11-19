from world import World 
import random
import numpy as np
from Qlearning import Qlearning
from policies import softmaxPolicy, epsGreedyPolicy, maxIndices
from pylab import *


runCount = 100
epiCount = 600


class SoftmaxPolicyOptAct:
	def __init__(self):
		self.actionList = []

	def policy(self,state,world, Q, tau):
		valuePerAction = [(Q[state,move],move) for move in world.moveList()]
		maxInd         = maxIndices(valuePerAction)
		action 		   = softmaxPolicy(state,world,Q,tau)
		maxActions	   = [valuePerAction[i][1] for i in maxInd]
		if action in maxActions:
			self.actionList += [1]
		else:
			self.actionList += [0]
		return action



figure()
ion()
show()
ylim(0,100)
labels =[]
for di, temperature in enumerate([0.1,0.5,0.9]):
	
	steps = np.zeros((runCount,epiCount))
	optim = np.zeros((runCount,epiCount))
	for i in range(runCount):
		cl = SoftmaxPolicyOptAct()
		steps[i,:] += np.array(Qlearning(epiCount,cl.policy,policyParam=temperature,initValue=5))
		print np.array(cl.actionList).shape
		optim[i,:] += np.array(cl.actionList)
		
	aveSteps = np.mean(steps, axis=0)
	aveOptimal = np.mean(optim, axis=0)

	t = range(1, aveSteps.shape[0]+1)
	labels += [r"$\tau = " +str(temperature)+ "$"]
	plot(t, aveOptimal)
	draw()

for di, epsilon in enumerate([0.1,0.3,0.5]):
	
	steps = np.zeros((runCount,epiCount))

	for i in range(runCount):
		steps[i,:] += np.array(Qlearning(epiCount,epsGreedyPolicy,policyParam=epsilon,initValue=5))
	
	aveSteps = np.mean(steps, axis=0)

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

# figure()
# t = range(1, devs.shape[1]+1)
# for i in range(4):
# 	plot(t, devs[i,:])

# ylim(0,300)
# plt.legend(labels)
# xlabel('episodes')
# ylabel('Deviation of steps per episode')
# title(r'Deviation of steps per episode with Q-learning with $\epsilon = ' + str(epsilon) + '$')
# grid(True)
# savefig("plots/dev2.2." + str(pli+1) + ".png")
# close()
