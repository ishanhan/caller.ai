import os
import jinja2
from flask import Flask, render_template, json, request, redirect, session
from jinja2 import Environment, FileSystemLoader
import speech_recognition as sr

app = Flask(__name__)
app.secret_key = 'ssh...Big secret!'
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

if __name__ == "__main__":
	app.debug = True
	app.run()
