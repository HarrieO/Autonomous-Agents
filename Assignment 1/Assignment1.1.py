from world    import World
from prey     import Prey
from predator import Predator
import numpy as np
		
runs = np.array([0]*100)
for i in range(100):
	runs[i] = World(Prey(0,0), Predator(5,5)).run();

print "100 runs completed"
print "Average number of steps per run: ", np.sum(runs)/100.0
print "Standard Deviation: ", np.std(runs)
print "Fastest run", min(runs)
print "Slowest run", max(runs)