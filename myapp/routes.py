from myapp import myapp_obj
from myapp.forms import LoginForm, SignupForm, EditProfile, AgencySignupForm, ListingForm
from flask import render_template, flash, redirect
from flask import Flask

from myapp import db
from myapp.models import User, Profile, Listing
from flask_login import current_user, login_user, logout_user, login_required



@myapp_obj.route("/")
def home():

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

@ myapp_obj.route("/agencysignup", methods=['GET', 'POST'])
def agencysignup():
    """
    This function returns the signup page with the SignUpForm

    Parameters:
    ----------
        none
    Return:
    ------
        redirects to login.html
    """
    form = AgencySignupForm()
    if form.validate_on_submit():
        flash(f'Welcome!')
        username = form.username.data
        email = form.email.data
        password = form.password.data
        agency = 'True'
        user = User(username, email)
        user.set_password(form.password.data)
        user.set_agency(agency)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template('agencysignup.html', form=form)

@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Incorrect username or password!', 'error')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        if user.agency == 'True':
            return redirect('/agencyprofile')
        if user.admin == 'True':
            return redirect('/adminprofile')
        else:
            return redirect('/profile')
    return render_template('login.html', form = form)

@myapp_obj.route("/profile")
@login_required
def profile():
    username = current_user.username
    agency = current_user.agency
    return render_template('profile.html', username = username, agency=agency)

@myapp_obj.route("/agencyprofile")
@login_required
def agencyprofile():
    username = current_user.username
    return render_template('agencyprofile.html', username = username)

@myapp_obj.route("/editprofile", methods=['GET', 'POST'])
@login_required
def edit():
    username = current_user.username
    user_id = current_user.id
    
    form = EditProfile()
    if form.validate_on_submit():
        flash(f'Changes Saved')
        first = form.first.data
        last = form.last.data
        phone = form.phone.data
        address1 = form.address1.data
        address2 = form.address2.data
        postal = form.postal.data
        state = form.state.data
        user_id = current_user.id
        profile = Profile(first, last, phone, address1, address2, postal, state, user_id)
        db.session.add(profile)
        db.session.commit()
        return redirect('/profile')
    profile = Profile.query.filter_by(user_id =current_user.id).first()
    return render_template('editprofile.html', form=form, username=username, profile=profile)

@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('home.html')

@myapp_obj.route("/createlisting", methods=['GET', 'POST'])
@login_required
def itemsForSale():
    form = ListingForm()
    user_id = current_user.id
    a = User.query.filter(User.agency =='True')
    form.agency.choices = a 
    if form.validate_on_submit():
        flash(f'Created!')
        name = form.name.data
        description = form.description.data
        location = form.location.data
        agency = form.agency.data
        warehouse = form.warehouse.data
        free = form.free.data
        trade = form.trade.data
        listing = Listing(name, description, location, agency, warehouse, free, trade, user_id)
        db.session.add(listing)
        db.session.commit()
        return redirect("/createditem")
    return render_template('listitem.html', a=a, form=form)

@myapp_obj.route("/createditem")
def itemTest():
    items = Listing.query.all()
    return render_template('testfile.html', items=items)
@myapp_obj.route('/sale')
def listings():
    return render_template('listings.html')

@myapp_obj.route('/adminprofile')
def adminprofile():
    return render_template('adminprofile.html')

@myapp_obj.route('/freelistings')
def freelistings():
    return render_template('freelistings.html')

@myapp_obj.route('/volunteer')
def volunteer():
    return render_template('VolunteerList.html')
