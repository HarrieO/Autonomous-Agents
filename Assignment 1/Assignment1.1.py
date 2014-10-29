from world    import World
from prey     import Prey
from predator import Predator
from agent    import Agent
import numpy as np
		
World(Prey(0,0), Agent(5,5)).run(worldPrint=True);

runs = np.array([0]*100)
for i in range(100):
	runs[i] = World(Prey(0,0), Agent(5,5)).run();

print "100 runs completed"
print "Average number of steps per run: ", np.sum(runs)/100.0
print "Standard Deviation: ", np.std(runs)
print "Fastest run", min(runs)
print "Slowest run", max(runs)