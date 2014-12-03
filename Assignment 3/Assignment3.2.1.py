from Qlearning import Qlearning
from policies import epsGreedyPolicy
import pylab as plt

#world = World((5,5),[(10,0),(0,10),(0,0),(10,10)])

predatorLocations = [(0,0),(10,10),(10,0),(0,10)]

episodes = 10000
steps, rewards = Qlearning(episodes, predatorLocations, epsGreedyPolicy)

for s,r in zip(steps,rewards):
    if r > 0:
        print s,"Caught!"
    else:
        print s

plt.scatter(range(episodes),rewards)
plt.show()
