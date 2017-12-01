import sys, math, numpy as np

#number pieces in a row to win
TARGET = 3
ROWS = 4
COLS = 4
DEEPEST = 3
next_actions = {}

#initialize depth to 0
def a_b_search(board, depth):
	assert len(board) == ROWS
	assert len(board[0]) == COLS
	v = max_value(board, -math.inf, math.inf, depth)
	return result(board, next_actions[v])

def max_value(board, a, b, depth):
	if depth == DEEPEST or is_win(board) or is_loss(board):
		return utility(board)
	v = -math.inf
	for action in actions(board):
		action_value = min_value(result(board, action, "X"), a, b, depth+1)
		if depth == 0:
			next_actions[action_value] = action
		v = max(v, action_value)
		if v >= b:
			return v
		a = max(a,v)
	return v

def min_value(board, a, b, depth):
	if depth == DEEPEST or is_loss(board) or is_win(board):
		return utility(board)
	v = math.inf
	for action in actions(board):
		v = min(v, max_value(result(board, action, "O"), a, b, depth+1))
		if v <= a:
			return v
		b = min(b,v)
	return v

#returns true if there is a four in a row (X's) on the board
def is_win(board):
	x_arr = []
	for i in range(0, TARGET):
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
	for i in range(0, TARGET):
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

#returns a list of numbers that represent possible actions (number 0-6)
def actions(board):
	ret = []
	for i in range(0, COLS):
		if board[0][i] == "":
			ret.append(i)
	return ret

#returns resulting board after taking an action (number from 0-6)
#type = string "X" or string "O"
def result(board, action, type):
	return

is_win([["","","","",],["","","",""],["","","",""],["X", "X", "X", "O"]])
