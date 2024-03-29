'''
Group 7
Carla Groenland   10208429
Harrie Oosterhuis 10196129
Fabian Voorter    10218807
'''
from world    import World
from prey     import Prey
from agent    import Agent
import numpy as np
		
World(Prey(0,0), Agent(5,5)).run(worldPrint=True);

# perform 100 runs and save the number of iterations in runs
runs = np.array([0]*100)
for i in range(100):
	runs[i] = World(Prey(0,0), Agent(5,5)).run();

print "100 runs completed"
print "Average number of steps per run: ", np.sum(runs)/100.0
print "Standard Deviation: ", np.std(runs)
print "Fastest run", min(runs)
print "Slowest run", max(runs)