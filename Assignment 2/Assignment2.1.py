import Qlearning as Q
import numpy as np
from pylab import *

runCount = 1000
for pli, alpha in enumerate([0.1,0.2,0.3,0.4,0.5]):
	figure()
	labels =[]
	devs = np.zeros((4,1000))
	for di, discount in enumerate([0.1,0.5,0.7,0.9]):
		
		steps = np.zeros((runCount,1000))

		for i in range(runCount):
			steps[i,:] += np.array(Q.Qlearning(1000,Q.epsGreedyPolicy,alpha=alpha,discount=discount))
		
		aveSteps = np.mean(steps, axis=0)
		devs[di,:]= np.std(steps, axis=0)

		t = range(1, aveSteps.shape[0]+1)
		labels += [r"$\gamma = " +str(discount)+ "$"]
		plot(t, aveSteps)




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

	plt.legend(labels)
	xlabel('episodes')
	ylabel('Average steps per episode')
	title(r'Average steps per episode with Q-learning with $\alpha = ' + str(alpha) + '$')
	grid(True)
	savefig("plots/dev2.1." + str(pli+1) + ".png")
	close()