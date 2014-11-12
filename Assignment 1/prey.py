'''
Group 7
Carla Groenland   10208429
Harrie Oosterhuis 10196129
Fabian Voorter    10218807
'''
from agent import Agent

class Prey(Agent):
	def __init__(self, x_init, y_init):
		Agent.__init__(self,x_init,y_init,"Prey")

	# return list of moves and the probability of each move
	# the prey has different moves than the predator, one difference being that the prey may not step on the predator
	def getMoveList(self, predatorLoc):
		moveList = [(0,1),(0,-1),(1,0),(-1,0)]
		for i in range(len(moveList)):
			if predatorLoc == self.locAfterMove(moveList[i]):
				del moveList[i]
				break
		prob 	 = 0.2/len(moveList)
		moveList = [(prob,move) for move in moveList ]
		moveList.append((0.8,(0,0)))

		return moveList
		
