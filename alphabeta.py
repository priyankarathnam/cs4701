import sys, math, numpy as np
from copy import copy, deepcopy

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
	if depth == DEEPEST or is_win(board, "X") or is_win(board, "O"):
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
	if depth == DEEPEST or is_win(board, "X") or is_win(board, "O"):
		return utility(board)
	v = math.inf
	for action in actions(board):
		v = min(v, max_value(result(board, action, "O"), a, b, depth+1))
		if v <= a:
			return v
		b = min(b,v)
	return v

#returns true if there is a four in a row (X's) on the board
def is_win(board, disc_type):
	arr = []
	for i in range(0, TARGET):
		arr.append(disc_type)
	np_arr = np.array(board)
	if num_matches(arr, np_arr) > 0:
		return True
	transposed = np_arr.transpose()
	if num_matches(arr, transposed) > 0:
		return True
	diags = [np_arr[::-1,:].diagonal(i) for i in range(-np_arr.shape[0]+1,np_arr.shape[1])]
	diags.extend(np_arr.diagonal(i) for i in range(np_arr.shape[1]-1,-np_arr.shape[0],-1))
	if num_matches(arr, diags) > 0:
		return True
	return False

#modified from https://stackoverflow.com/questions/42107865/python-numpy-array-sublist-match-with-large-list-where-sequence-matter
def num_matches(sublist, matrix):
	count = 0;
	n = len(sublist)
	for row in matrix:
		for i in range(len(row)-n+1):
			if (sublist==row[i:i+n]).all():
				count+=1
	return count

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

#returns resulting board (without modifying the old board) after taking an 
# action (number from 0-6)
# disc_type = string "X" or string "O"
def result(board, action, disc_type):
	new_board = deepcopy(board)
	i = ROWS - 1
	while i >= 0:	
		if (new_board[i][action] != ""):
			if i == 0:
				print("ILLEGAL ACTION. COLUMN " + str(action) + " IS ALREADY FILLED.")
			i -= 1
		else:
			new_board[i][action] = disc_type
			return new_board
	return new_board

is_win([["","","","",],["","","",""],["","","",""],["X", "X", "X", "O"]])
board = [["","","","",],["","","",""],["","","",""],["X", "X", "X", "O"]]
action = 3
disc_type = "O"
