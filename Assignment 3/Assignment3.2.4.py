import pylab as pl
import numpy as np
from world import World
from minimax import minimax
from scipy import ndimage

episodes = 10
runs = 1

steps = np.zeros((episodes))
for i in range(runs):
    print "run",i
    steps += minimax(episodes,[(0,0)],0.1, 0.99999, 0.9, 1.0)[0]

steps /= runs

steps = ndimage.filters.gaussian_filter(steps)

pl.title('Number of iterations per episode using Minimax.')
pl.ylabel('Iterations')
pl.xlabel('Episodes')
pl.plot(range(len(steps)), steps)
pl.savefig("plots/longrun322.png")
