from world import World 
import random
import numpy as np
from Qlearning import Qlearning
from MCon import MCon
from MCoff import MCoff
from sarsa import sarsa
from policies import softmaxPolicy, epsGreedyPolicy, maxIndices
from pylab import *

runCount = 100
epiCount = 600
figure()

labels =[]


for di, epsilon in enumerate([0.1]):
	
	steps = np.zeros((runCount,epiCount))
	for i in range(runCount):
		steps[i,:] = np.array(MCoff(epiCount,initValue=5))		
	aveSteps = np.mean(steps, axis=0)

	t = range(1, aveSteps.shape[0]+1)
	labels += ["MC off-policy"]
	plot(t, aveSteps)
	draw()

for di, epsilon in enumerate([0.1]):
	
	steps = np.zeros((runCount,epiCount))
	for i in range(runCount):
		steps[i,:] = np.array(MCon(epiCount,alpha=0.5,epsilon=epsilon,initValue=5))		
	aveSteps = np.mean(steps, axis=0)

	t = range(1, aveSteps.shape[0]+1)
	labels += ["MC on-policy"]
	plot(t, aveSteps)
	draw()


for di, epsilon in enumerate([0.1]):
	
	steps = np.zeros((runCount,epiCount))
	for i in range(runCount):
		steps[i,:] = np.array(sarsa(epiCount,epsGreedyPolicy,policyParam=epsilon,alpha=0.5,initValue=5))		
	aveSteps = np.mean(steps, axis=0)

	t = range(1, aveSteps.shape[0]+1)
	labels += ["Sarsa"]
	plot(t, aveSteps)
	draw()

for di, epsilon in enumerate([0.1]):
	
	steps = np.zeros((runCount,epiCount))
	for i in range(runCount):
		steps[i,:] = np.array(Qlearning(epiCount,epsGreedyPolicy,policyParam=epsilon,alpha=0.5,initValue=5))		
	aveSteps = np.mean(steps, axis=0)

	t = range(1, aveSteps.shape[0]+1)
	labels += ["Qlearning"]
	plot(t, aveSteps)
	draw()



plt.legend(labels)
xlabel('episodes')
ylabel('Average steps per episode')
title(r'Average steps per episode with Q-learning with softmax-policy.')
grid(True)
ylim(0,250)
savefig("plots/steps2.4.1.png")
xlim(0,100)
savefig("plots/steps2.4.2.png")
close()
