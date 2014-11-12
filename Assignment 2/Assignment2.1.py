import Qlearning as Q
import numpy as np
from pylab import *

runCount = 200
for alpha in [0.1,0.2,0.3,0.4,0.5]:
	for discount in [0.1,0.5,0.7,0.9]:
		
		aveSteps = np.zeros(1000)

		for i in range(runCount):
			aveSteps += np.array(Q.Qlearning(1000,Q.epsGreedyPolicy,alpha=alpha,discount=discount))
		aveSteps /= runCount

		t = range(1, aveSteps.shape[0]+1)
		plot(t, aveSteps)

	xlabel('episodes')
	ylabel('Average steps per episode')
	title('Average steps per episode with Q-learning.')
	grid(True)
	savefig("Ass2.1.png")
	show()
