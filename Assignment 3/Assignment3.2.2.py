import pylab as pl
import numpy as np
from world import World
from minimax import minimax


w = World((5,5),[(0,0),(0,10),(10,0),(10,10)])

print minimax(10,[(0,0)],0.1, 0.98, 0.9)