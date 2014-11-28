from world import World 
from policies import epsGreedyPolicy, maxIndices
import numpy as np
import random


def randomPolicy():
	world = World((0,0),(1,1))
	movelist = world.moveList()
	behaPolicy = {}
	for state in world.allStates():
		for move in movelist:
			behaPolicy[(state, move)] = 1.0/len(movelist)
	return behaPolicy

def horizontalHeuristicPolicy():
	world = World((0,0),(1,1))
	movelist = world.moveList()
	behaPolicy = {}
	for state in world.allStates():
		if state[0] > 0:
			bestMove = (-1,0)
		elif state[0] < 0:
			bestMove = (1,0)
		elif state[1] > 0:
			bestMove = (0,-1)
		else:
			bestMove = (0,1)
		for move in movelist:
			if move == bestMove:
				behaPolicy[(state, move)] = 0.9
			else:
				behaPolicy[(state, move)] = 0.1/(len(movelist)-1)
	return behaPolicy

def epsilonGreedyPolicy():
	world = World((0,0),(1,1))
	movelist = world.moveList()
	behaPolicy = {}
	for state in world.allStates():
		bestMoves = []
		if state[0] > 0:
			bestMoves.append((-1,0))
		elif state[0] < 0:
			bestMoves.append(( 1,0))
		if state[1] > 0:
			bestMoves.append((0,-1))
		elif state[1] > 0:
			bestMoves.append((0, 1))
		for move in movelist:
			if move in bestMoves:
				behaPolicy[(state, move)] = 0.9/len(bestMoves)
			else:
				behaPolicy[(state, move)] = 0.1/(len(movelist)-len(bestMoves))
	return behaPolicy
