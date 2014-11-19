import numpy as np
from pylab import *
from Qlearning import Qlearning
from policies import epsGreedyPolicy

runCount = 100
epiCount = 600
for pli, alpha in enumerate([1,0.9,0.7,0.5,0.4,0.3,0.2,0.1]):
	figure()
	labels =[]
	devs = np.zeros((6,epiCount))
	for di, discount in enumerate([0.9,0.7,0.5,0.1]):
		
		steps = np.zeros((runCount,epiCount))

		for i in range(runCount):
			steps[i,:] += np.array(Qlearning(epiCount,epsGreedyPolicy,alpha=alpha,discount=discount))
		
		aveSteps = np.mean(steps, axis=0)
		devs[di,:]= np.std(steps, axis=0)

		t = range(1, aveSteps.shape[0]+1)
		labels += [r"$\gamma = " +str(discount)+ "$"]
		plot(t, aveSteps)



	ylim(0,300)
	plt.legend(labels)
	xlabel('episodes')
	ylabel('Average steps per episode')
	title(r'Average steps per episode with Q-learning with $\alpha = ' + str(alpha) + '$')
	grid(True)
	savefig("plots/ave2.1." + str(pli+1) + ".png")
	close()

	figure()
	t = range(1, devs.shape[1]+1)
	for i in range(4):
		plot(t, devs[i,:])

	ylim(0,300)
	plt.legend(labels)
	xlabel('episodes')
	ylabel('Average steps per episode')
	title(r'Average steps per episode with Q-learning with $\alpha = ' + str(alpha) + '$')
	grid(True)
	savefig("plots/dev2.1." + str(pli+1) + ".png")
	close()
