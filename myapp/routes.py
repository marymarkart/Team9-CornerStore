from myapp import myapp_obj
from myapp.forms import LoginForm
from flask import render_template, flash, redirect
from flask import Flask

from myapp import db
from myapp.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required


@myapp_obj.route("/tester")
def tester():
	x = 'dollar'
	return render_template('home.html')

@myapp_obj.route("/signup")
def signup():
	return render_template('signup.html')

@myapp_obj.route("/quiz")
def quiz(flask):
	myList = ['Lisa', 'Linh', 'Emily']
	return render_template('quiz.html', names=myList)

@myapp_obj.route("/login")
def login():
	return render_template('login.html')
