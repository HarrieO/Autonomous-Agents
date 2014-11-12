import Qlearning as Q
import numpy as np
from pylab import *

runCount = 20
for alpha in range(0.1,0.6,0.1):
	aveSteps = np.zeros(1000)

	for i in range(runCount):
		aveSteps += np.array(Q.Qlearning(1000,Q.epsGreedyPolicy,alpha=alpha))
	aveSteps /= runCount

	t = range(1, aveSteps.shape[0]+1)
	plot(t, aveSteps)

xlabel('episodes')
ylabel('Average steps per episode')
title('Average steps per episode with Q-learning.')
grid(True)
savefig("Ass2.1.png")
show()
