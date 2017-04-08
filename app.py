import os
from flask import Flask, render_template, json, request, redirect, session
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)
app.secret_key = 'ssh...Big secret!'
#MySQL configurations



# route to index.html
@app.route("/")
def main():
    return render_template('index.html')

# route to signup.html
@app.route('/showRec')
def showSignUp():
    return render_template('record.html')

# interact with MySQL for sign up


if __name__ == "__main__":
    app.debug = True
    app.run()
