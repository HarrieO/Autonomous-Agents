from Qlearning import Qlearning
from policies import epsGreedyPolicy
import pylab as pl
import numpy as np

ax = pl.subplot(111)
pl.title('Probability of episode ending with prey caught.')
pl.ylabel('Prey caught ratio')
pl.xlabel('Episodes')
predatorLocations = [(0,0),(10,0),(0,10),(10,10)]
episodes = 10000
runs = 200
labels = []
avesteps = np.zeros((4,episodes))
avestepscatch = np.zeros((4,episodes))
avestepscrash = np.zeros((4,episodes))
avecatch = np.zeros((4,episodes))
for predators in range(1,5)[::-1]:
    totalcatch = np.zeros((episodes))
    for i in range(runs):
        steps, rewards = Qlearning(episodes, predatorLocations[:predators], epsGreedyPolicy)
        steps   = np.array(steps)
        rewards = np.array(rewards)
        avesteps[predators-1,:] += steps
        avecatch[predators-1,:] += rewards
        avestepscatch[predators-1,rewards>0] += steps[rewards>0]
        avestepscrash[predators-1,rewards<=0] += steps[rewards<=0]
        totalcatch[rewards>0]   += 1
        print predators, i

    avecatch[predators-1,:] /= runs
    avesteps[predators-1,:] /= runs
    avestepscatch[predators-1,:] /= totalcatch
    if predators > 1:
        avestepscrash[predators-1,:] /= (runs-totalcatch)
    pl.plot(range(episodes),avecatch[predators-1,:])
    labels.append(str(predators) + " predators")


# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(labels,loc='center left', bbox_to_anchor=(1, 0.5))

pl.savefig("plots/ratio321.png")
pl.close()

pl.figure()
ax = pl.subplot(111)
pl.title('Average number of iterations per episode.')
pl.ylabel('Iterations in episode')
pl.xlabel('Episodes')
for predators in range(1,5):
    pl.plot(range(episodes),avesteps[predators-1,:])

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(labels,loc='center left', bbox_to_anchor=(1, 0.5))
pl.savefig("plots/steps321.png")

pl.figure()
ax = pl.subplot(111)
pl.title('Average number of iterations per episode ending with prey caught.')
pl.ylabel('Iterations in episode')
pl.xlabel('Episodes')
for predators in range(2,5):
    ind = np.logical_not(np.isnan(avestepscatch[predators-1,:]))
    pl.plot(np.arange(episodes)[ind],avestepscatch[predators-1,ind])

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(labels[:-1],loc='center left', bbox_to_anchor=(1, 0.5))
pl.savefig("plots/stepscatch321.png")


pl.figure()
ax = pl.subplot(111)
pl.title('Average number of iterations per episode ending with prey uncaught.')
pl.ylabel('Iterations in episode')
pl.xlabel('Episodes')
for predators in range(2,5):
    ind = np.logical_not(np.isnan(avestepscrash[predators-1,:]))
    pl.plot(np.arange(episodes)[ind],avestepscrash[predators-1,ind])

# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
ax.legend(labels[:-1],loc='center left', bbox_to_anchor=(1, 0.5))
pl.savefig("plots/stepscrash321.png")