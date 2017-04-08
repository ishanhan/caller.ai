import os
import sys
import requests
import json
import random

from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, FileSystemLoader
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = 'ssh...Big secret!'
access_token = 'N6M4FKPZHGZHEMZH5EY3URDVCIILRBRE'
#MySQL configurations



# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to signup.html
@app.route('/showRec')
def showRecord():
	
   	r = sr.Recognizer()
	m = sr.Microphone()
	value = ""
	try:
		with m as source: r.adjust_for_ambient_noise(source)
	
		print "Say Something!"
		with m as source: audio = r.listen(source)
		print("Set minimum energy threshold to {}".format(r.energy_threshold))
		print "Got It!"
		try:
			value = r.recognize_google(audio)
			print value
			
		except sr.UnknownValueError:
			print("Oops! Didn't catch that")
	except:
		pass
	return render_template('record.html', value = value)

# interact with Wit.ai
@app.route('/wit')
def useWit():

	"""
	curl \
 	-H 'Authorization: Bearer J3H7YDLBJZZK5PFBEU5OTWXHNOZ6GEAJ' \
	'https://api.wit.ai/message?v=20170408&q='
	"""
	session_id = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))

	while True:
		message_body = "my transaction failed"
		print session_id
		response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session_id+'&q='+message_body,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer N6M4FKPZHGZHEMZH5EY3URDVCIILRBRE"})
		dict_response = json.loads(response.text)
		print dict_response
		if dict_response['type']=="stop":
			break

	intent = None
	confidence = None
	entities = None
	msg = None

	# if dict_response['entities']['intent']:
	# 	intent = dict_response['entities']['intent'][0]['value']
	# 	confidence = dict_response['entities']['intent'][0]['confidence']
	# 	entities = dict_response['entities']

	# print intent
	# print confidence
	# print entities
	return render_template('wit.html',output = dict_response, input = message_body)


	
if __name__ == "__main__":
	app.debug = True
	app.run()
