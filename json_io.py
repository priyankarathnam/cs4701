#!flask/bin/python

import sys, math, numpy as np
from copy import copy, deepcopy

from flask import Flask, render_template, request, redirect, Response, jsonify
import random, json

#number pieces in a row to win
TARGET = 4
ROWS = 6
COLS = 7
DEEPEST = 3
OFFENSE_PATTERNS = {"almost_win": ["","X","X","X",""], "three_x1": ["X","X","X",""], "three_x2": ["X","X","","X"], "two_x1": ["X", "","X",""], "two_x2": ["","X","X",""], "two_x3": ["X","X","",""]}
DEFENSE_PATTERNS = {"almost_loss": ["","O","O","O",""], "three_o1": ["O","O","O",""], "three_o2": ["O","O","","O"], "two_o1": ["O", "","O",""], "two_o2": ["","O","O",""], "two_o3": ["O","O","",""]}
OFFENSE_SCORES = {"almost_win": 1000, "three_x1": 100, "three_x2": 100, "two_x1": 10, "two_x2": 10, "two_x3": 10}
DEFENSE_SCORES = {"almost_loss": -3000, "three_o1": -300, "three_o2": -300, "two_o1": -30, "two_o2": -30, "two_o3": -30}
next_actions = {}

app = Flask(__name__)

@app.route('/')
def output():
	# serve index template
	return render_template('index.html', name='Joe')

@app.route('/receiver', methods = ['POST', 'GET'])
def worker():
	# read json + reply
	# if request.method=='POST':
		data = request.get_json(force=True)
		result = []

		for item in data:
			# loop over every row
			result.append([str(item['0']),str(item['1']),str(item['2']),str(item['3']),str(item['4']),str(item['5']),str(item['6'])])
		print("before my move: ")
		print(result)
		result = a_b_search(result, 0)
		if is_win(result, "X"):
			result.append(["win"])
			return jsonify(result)
		return jsonify(result)
	# else:
	# 	return "ok"
@app.route('/receiver2', methods = ['POST', 'GET'])
def worker2():
	# read json + reply
	# if request.method=='POST':
		data = request.get_json(force=True)
		result = []

		for item in data:
			# loop over every row
			result.append([str(item['0']),str(item['1']),str(item['2']),str(item['3']),str(item['4']),str(item['5']),str(item['6'])])
		if is_win(result, "O"):
			return jsonify("loss")
		return jsonify("no loss")
	# else:
	# 	return "ok"
#initialize depth to 0
def a_b_search(board, depth):
	assert len(board) == ROWS
	assert len(board[0]) == COLS
	v = max_value(board, -math.inf, math.inf, depth)
	print(next_actions)
	return result(board, next_actions[v], "X")

def max_value(board, a, b, depth):
	if depth == DEEPEST or is_win(board, "X") or is_win(board, "O"):
		print("terminal test")
		if is_win(board, "O"):
			print(-math.inf)
			return -math.inf
		if is_win(board, "X"):
			print(math.inf)
			return math.inf
		print(utility(board))
		return utility(board)
	v = -math.inf
	#print("actions: "+str(actions(board)))
	for action in actions(board):
		print("depth: "+str(depth))
		print("action: "+str(action))
		print(result(board, action, "X"))
		action_value = min_value(result(board, action, "X"), a, b, depth+1)
		#print("action value: "+str(action_value))
		if depth == 0:
			next_actions[action_value] = action
		v = max(v, action_value)
		if v >= b:
			return v
		a = max(a,v)
	return v

def min_value(board, a, b, depth):
	if depth == DEEPEST or is_win(board, "X") or is_win(board, "O"):
		print("terminal test")
		if is_win(board, "O"):
			print(-math.inf)
			return -math.inf
		if is_win(board, "X"):
			print(math.inf)
			return math.inf
		print(utility(board))
		return utility(board)
	v = math.inf
	for action in actions(board):
		print("depth: "+str(depth))
		print("action: "+str(action))
		print(result(board, action, "O"))
		v = min(v, max_value(result(board, action, "O"), a, b, depth+1))
		if v <= a:
			return v
		b = min(b,v)
	return v

#returns true if there is a four in a row for the specific disc type on the board
def is_win(board, disc_type):
	assert disc_type == "O" or disc_type == "X"
	arr = []
	for i in range(0, TARGET):
		arr.append(disc_type)
	np_arr = np.array(board)
	if num_matches(arr, np_arr) > 0:
		return True
	transposed = np_arr.transpose()
	if num_matches(arr, transposed) > 0:
		return True
	#diags code from https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
	diags = [np_arr[::-1,:].diagonal(i) for i in range(-np_arr.shape[0]+1,np_arr.shape[1])]
	diags.extend(np_arr.diagonal(i) for i in range(np_arr.shape[1]-1,-np_arr.shape[0],-1))
	if num_matches(arr, diags) > 0:
		return True
	return False

def is_symmetric(sublist):
	if len(sublist) <= 1:
		return True
	if sublist[0] != sublist[-1]:
		return False
	else:
		return is_symmetric(sublist[1:-1])

#find number of times sublist appears on board in all directions
def test_directions(board, sublist):
	count = 0
	np_arr = np.array(board)
	transposed = np_arr.transpose()
	#diags code from https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python
	diags = [np_arr[::-1,:].diagonal(i) for i in range(-np_arr.shape[0]+1,np_arr.shape[1])]
	diags.extend(np_arr.diagonal(i) for i in range(np_arr.shape[1]-1,-np_arr.shape[0],-1))
	count += (num_matches(sublist, np_arr)+num_matches(sublist, transposed)+num_matches(sublist, diags))
	if not is_symmetric(sublist):
		sublist.reverse()
		count += (num_matches(sublist, np_arr)+num_matches(sublist, transposed)+num_matches(sublist, diags))
	return count

#returns the number of matches between the sublist and each row of the matrix
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
	total = 0
	#offense
	for pattern in OFFENSE_PATTERNS.keys():
		num = test_directions(board, OFFENSE_PATTERNS[pattern])
		if not num == 0:
			total+=OFFENSE_SCORES[pattern]*num
		if total == math.inf:
			return total
	#defense
	for pattern in DEFENSE_PATTERNS.keys():
		num = test_directions(board, DEFENSE_PATTERNS[pattern])
		if not num == 0:
			total+=DEFENSE_SCORES[pattern]*num
		if total == -math.inf:
			return total
	return total

#returns score for this state (heuristic)
# def min_utility(board):	
# 	total = 0
# 	#defense
# 	for pattern in DEFENSE_PATTERNS.keys():
# 		num = test_directions(board, DEFENSE_PATTERNS[pattern])
# 		if not num == 0:
# 			total+=DEFENSE_SCORES[pattern]*num
# 		if total == -math.inf:
# 			return total
# 	#offense
# 	for pattern in OFFENSE_PATTERNS.keys():
# 		num = test_directions(board, OFFENSE_PATTERNS[pattern])
# 		if not num == 0:
# 			total+=OFFENSE_SCORES[pattern]*num
# 		if total == math.inf:
# 			return total
# 	return total

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
	assert type(action) == int and action >= 0 and action < COLS
	assert disc_type == "O" or disc_type == "X"
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

if __name__ == '__main__':
	# run!
	app.run()