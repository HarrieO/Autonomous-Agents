from world import World 

world = World((0,0),(1,1))

print world.position
for i in range(15):
	print world.posAfterPreyMove((1,0))
	world.preyMove((1,0))