from agent import Agent

class Prey(Agent):
	def __init__(self, x_init, y_init):
		Agent.__init__(self,x_init,y_init,"Prey")

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
		
