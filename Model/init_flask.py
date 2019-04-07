from flask import Flask, url_for, request, render_template, request, redirect, Response
import random, json, sys


app = Flask(__name__)

@app.route('/')
def output():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/receiver', methods = ['POST'])
def worker():
	# read json + reply
	data = request.get_json(force=True)
	result = ''

	for item in data:
		# loop over every row
		make = str(item['make'])
		if(make == 'Porsche'):
			result += make + ' -- That is a good manufacturer\n'
		else:
			result += make + ' -- That is only an average manufacturer\n'

	return result


if __name__ == "__main__":
	app.run()