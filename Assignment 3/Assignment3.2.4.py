import pylab as pl
import numpy as np
from Qlearning import Qlearning
from policies import epsGreedyPolicy
from world import World
from minimax import minimax
from scipy import ndimage

episodes = 10000
runs = 10

steps = np.zeros((episodes))
for i in range(runs):
    print "run",i
    steps += Qlearning(episodes, [(0,0)], epsGreedyPolicy,alpha_pred=0.2,alpha_prey=0.2)[0]

steps /= runs

steps = ndimage.filters.gaussian_filter(steps,4)
pl.plot(range(len(steps)), steps)

steps = np.zeros((episodes))
for i in range(runs):
    print "run",i
    steps += minimax(episodes,[(0,0)],0.1, 0.99999, 0.9)[0]

steps /= runs

steps = ndimage.filters.gaussian_filter(steps,4)
pl.plot(range(len(steps)), steps)

pl.legend(["Q-learning","Minimax"])
pl.title('Number of iterations per episode using Minimax and Q-learning.')
pl.ylabel('Iterations')
pl.xlabel('Episodes')
pl.savefig("plots/equalminimax.png")
pl.ylim(0,200)
pl.savefig("plots/equalminimaxzoom.png")
pl.close()

pl.plot(range(len(steps)), steps)

steps = np.zeros((episodes))
for i in range(runs):
    print "run",i
    steps += minimax(episodes,[(0,0)],0.1, 0.99999, 0.9, 0.1, 1.0)[0]

steps /= runs

steps = ndimage.filters.gaussian_filter(steps,4)


pl.plot(range(len(steps)), steps)

steps = np.zeros((episodes))
for i in range(runs):
    print "run",i
    steps += minimax(episodes,[(0,0)],0.1, 0.99999, 0.9, 1.0, 0.1)[0]

steps /= runs

steps = ndimage.filters.gaussian_filter(steps,4)

pl.plot(range(len(steps)), steps)
pl.legend(["Prey=Pred","Prey>Pred","Prey<Pred"])
pl.title('Number of iterations per episode using Minimax for different learning rates.')
pl.ylabel('Iterations')
pl.xlabel('Episodes')
pl.savefig("plots/easyminimax.png")
