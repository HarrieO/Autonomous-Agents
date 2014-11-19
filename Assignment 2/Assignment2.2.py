import numpy as np
from pylab import *
from Qlearning import Qlearning
from policies import epsGreedyPolicy

runCount = 50
epiCount = 600
for pli, epsilon in enumerate([0.7,0.5,0.2,0.1,0.0]):
	figure()
	labels =[]
	devs = np.zeros((5,epiCount))
	for di, initValue in enumerate([-15,0,5,10,15]):
		
		steps = np.zeros((runCount,epiCount))

		for i in range(runCount):
			steps[i,:] += np.array(Qlearning(epiCount,epsGreedyPolicy,policyParam=epsilon,initValue=initValue))
		
		aveSteps = np.mean(steps, axis=0)
		devs[di,:]= np.std(steps, axis=0)

		t = range(1, aveSteps.shape[0]+1)
		labels += [r"$init-Value = " +str(initValue)+ "$"]
		plot(t, aveSteps)



	ylim(0,300)
	plt.legend(labels)
	xlabel('episodes')
	ylabel('Average steps per episode')
	title(r'Average steps per episode with Q-learning with $\epsilon = ' + str(epsilon) + '$')
	grid(True)
	savefig("plots/ave2.2." + str(pli+1) + ".png")
	close()

	figure()
	t = range(1, devs.shape[1]+1)
	for i in range(4):
		plot(t, devs[i,:])

	ylim(0,300)
	plt.legend(labels)
	xlabel('episodes')
	ylabel('Deviation of steps per episode')
	title(r'Deviation of steps per episode with Q-learning with $\epsilon = ' + str(epsilon) + '$')
	grid(True)
	savefig("plots/dev2.2." + str(pli+1) + ".png")
	close()