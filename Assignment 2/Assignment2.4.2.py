import numpy as np
from MCoff import MCoff
from pylab import *
from behaviours import *

runCount = 5
epiCount = 10000
figure()

labels =[]
aveMatches =[]

for name, policy in zip(["Random","Heuristic","Epsilon Greedy"],[randomPolicy(),horizontalHeuristicPolicy(),epsilonGreedyPolicy()]):
	
	steps = np.zeros((runCount,epiCount))
	match = np.zeros((runCount,epiCount))
	for i in range(runCount):
		matches = []
		steps[i,:] = np.array(MCoff(epiCount,policy,matches=matches,initValue=5))
		match[i,:] = np.array(matches)
		print name, i
	aveSteps = np.mean(steps, axis=0)
	aveMatches.append(np.mean(match, axis=0))

	t = range(1, aveSteps.shape[0]+1)
	labels += [name]
	plot(t, aveSteps)


plt.legend(labels)
xlabel('episodes')
ylabel('Average steps per episode')
title(r'Average steps per episode with Monte Carlo Off-Policy.')
grid(True)
savefig("plots/steps2.4.4.png")
close()

for ave in [aveMatches[0],aveMatches[2],aveMatches[1]]:
	plot(t, ave)

plt.legend([labels[0],labels[2],labels[1]])
xlabel('episodes')
ylabel('Average matching (state, actions) per episode')
title(r'Average matching state-action pairs per episode.')
grid(True)
savefig("plots/steps2.4.5.png")
close()