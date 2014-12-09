from world import World
import random
import pylab as pl

#world = World((5,5),[(10,0),(0,10),(0,0),(10,10),(10,1),(0,9),(0,1),(10,9)])

predatorLocations = [(0,0),(0,10),(10,0),(10,10)]
preds = []
iters = []
prey  = []
for no in range(len(predatorLocations)):
    world = World((5,5),predatorLocations[:no+1])

    allMoves    = world.allMoveList()
    singleMoves = world.singleMoveList()

    runs            = 1000
    totalCaughtPrey = 0
    totalIterations = 0
    for i in range(runs):
        world      = World((5,5),predatorLocations[:no+1])
        iterations = 0
        while not world.stopState():
            preyMove      = random.choice(singleMoves)
            predatorMoves = random.choice(allMoves)
            reward        = world.move(preyMove,predatorMoves)
            iterations   += 1
    
        if reward[0] < 0:
            totalCaughtPrey += 1
        totalIterations += iterations

    print "Number of predators", no+1,
    preds.append(no+1)
    print "Average Iterations", totalIterations/float(runs),
    iters.append(totalIterations/float(runs))
    print "chance of catching prey", totalCaughtPrey/float(runs)
    prey.append(totalCaughtPrey/float(runs))

pl.scatter(preds,prey)
pl.plot(preds,prey)
pl.ylabel('Prey caught ratio')
pl.xlabel('Number of predators')
pl.show()
