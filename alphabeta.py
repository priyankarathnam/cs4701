import sys, math, numpy as np

#number pieces in a row to win
target = 3
rows = 4
cols = 4
next_actions = {}

#initialize depth to 0
def a_b_search(board, depth):
	assert len(board) == rows
	assert len(board[0]) == cols
	v = max_value(board, -math.inf, math.inf, depth)
	return result(board, next_actions[v])

def max_value(board, a, b, depth):
	if depth == 3 or is_win(board):
		return utility(board)
	v = -math.inf
	for action in actions(board):
		action_value = min_value(result(board, action), a, b, depth+1)
		if depth == 0:
			next_actions[action_value] = action
		v = max(v, action_value)
		if v >= b:
			return v
		a = max(a,v)
	return v

def min_value(board, a, b, depth):
	if depth == 3 or is_loss(board):
		return utility(board)
	v = math.inf
	for action in actions(board):
		v = min(v, max_value(result(board, action), a, b, depth+1))
		if v <= a:
			return v
		b = min(b,v)
	return v

#returns true if there is a four in a row (X's) on the board
def is_win(board):
	x_arr = []
	for i in range(0, target):
		x_arr.append("X")
	if x_arr in board:
		return True
	np_arr = np.array(board)
	transposed = np_arr.transpose()
	if x_arr in transposed.tolist():
		return True
	diags = [np_arr[::-1,:].diagonal(i) for i in range(-np_arr.shape[0]+1,np_arr.shape[1])]
	diags.extend(np_arr.diagonal(i) for i in range(np_arr.shape[1]-1,-np_arr.shape[0],-1))
	diags = [n.tolist() for n in diags]
	if x_arr in diags:
		return True
	return False

#returns true if there is a four in a row (O's) on the board
def is_loss(board):
	o_arr = []
	for i in range(0, target):
		o_arr.append("O")
	if o_arr in board:
		return True
	np_arr = np.array(board)
	transposed = np_arr.transpose()
	if o_arr in transposed.tolist():
		return True
	diags = [np_arr[::-1,:].diagonal(i) for i in range(-np_arr.shape[0]+1,np_arr.shape[1])]
	diags.extend(np_arr.diagonal(i) for i in range(np_arr.shape[1]-1,-np_arr.shape[0],-1))
	diags = [n.tolist() for n in diags]
	if o_arr in diags:
		return True
	return False

#returns score for this state (heuristic)
def utility(board):
	return

#returns a list of numbers that represent possible actions (0-6)
def actions(board):
	return

#returns resulting board after taking an action (number from 0-6)
def result(board, action):
	return
is_win([["","","","",],["","","",""],["","","",""],["X", "X", "X", "O"]])
