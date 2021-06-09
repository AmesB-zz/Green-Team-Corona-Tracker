'''
this part of app sets base for app and lands all users on homepage
'''


from flask import (
    Flask, render_template, redirect, url_for, request,
)

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('login.html')

@app.route('/create_account')
def create_account():
    return render_template('create_account.html')




