from world import World 
import random
import numpy as np
from Qlearning import Qlearning
from policies import softmaxPolicy



print Qlearning(10, softmaxPolicy)
