from flask import (
    Flask, render_template, redirect, url_for, request
)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('login.html')

'''
@app.route('/')
def hello_world():
    return 'Hello, World!'
'''