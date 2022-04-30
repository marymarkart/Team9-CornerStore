from myapp import myapp_obj
from myapp.forms import LoginForm, SignupForm
from flask import render_template, flash, redirect
from flask import Flask

from myapp import db
from myapp.models import User
from flask_login import current_user, login_user, logout_user, login_required


@myapp_obj.route("/tester")
def tester():
	x = 'dollar'
	return render_template('home.html')

@ myapp_obj.route("/signup", methods=['GET', 'POST'])
def signup():
    """
    This function returns the signup page with the SignUpForm

    Parameters:
    ----------
        none
    Return:
    ------
        redirects to login.html
    """
    form = SignupForm()
    if form.validate_on_submit():
        flash(f'Welcome!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username, email)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template('signup.html', form=form)



@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Incorrect username or password!', 'error')
			return redirect('/login')
		login_user(user, remember=form.remember_me.data)

		# exists = db.session.query(Activity.id).filter(
		# 	Activity.owner_id == user.id).order_by(desc(Activity.id)).first() is not None
		# if exists:
		# 	user_activity = Activity.query.filter(
		# 		Activity.owner_id == user.id).order_by(desc(Activity.id)).first()
		# 	user_time = user_activity.usertime.strftime("%m-%d-%y")
		# 	today = datetime.datetime.utcnow().strftime("%m-%d-%y")
		# 	if user_time != today:
		# 		time_login = Activity(timeamount=0, owner=user)
		# 		db.session.add(time_login)
		# 		db.session.commit()
		# else:
		# 	time_login = Activity(timeamount=0, owner=user)
		# 	db.session.add(time_login)
		# 	db.session.commit()

		return redirect('/profile')
	return render_template('login.html', form=form)


@myapp_obj.route("/profile")
def profile():
	return render_template('profile.html')
