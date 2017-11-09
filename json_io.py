#!flask/bin/python

import sys

from flask import Flask, render_template, request, redirect, Response
import random, json

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
		result = ''

		for item in data:
			# loop over every row
			result += str(item['make']) + '\n'

		print(result)
		return result
	# else:
	# 	return "ok"

if __name__ == '__main__':
	# run!
	app.run()