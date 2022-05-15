from sqlalchemy import null
from app import myapp_obj
from app.forms import LoginForm, SignupForm, EditProfile, AgencySignupForm, ListingForm, VolunteerForm, NewName, NewDesc, NewPrice, ReviewForm
from flask import render_template, flash, redirect
from flask import Flask, url_for

from app import db
from app.models import User, Profile, Listing, Volunteer, BeVolunteer, Rating
from flask_login import current_user, login_user, logout_user, login_required
import stripe
import os


@myapp_obj.route("/")
def home():

	return render_template('home.html')

"""




SIGN UP




"""

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


"""



LOGIN / LOGOUT



"""

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


@myapp_obj.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('home.html')


"""



PROFILES




"""

@myapp_obj.route("/profile")
@login_required
def profile():
    username = current_user.username
    user_id = current_user.id
    agency = current_user.agency
    admin = current_user.admin
    if agency == 'True':
        return redirect('/agencyprofile')
    if admin == 'True':
        return redirect('/adminprofile')

    listings = Listing.query.filter(Listing.user_id==user_id)
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
    return render_template('profile.html', username = username, agency=agency, listings=listings, count=count, sold=sold)

@myapp_obj.route("/agencyprofile")
@login_required
def agencyprofile():
    username = current_user.username
    user_id = current_user.id
    listings = Volunteer.query.filter(Volunteer.user_id==user_id)
    return render_template('agencyprofile.html', username = username, listings=listings)

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



@myapp_obj.route('/adminprofile')
@login_required
def adminprofile():
    return render_template('adminprofile.html')

@myapp_obj.route('/viewprofile/<int:val>')
def viewProfile(val):
    user = User.query.get(val)
    print(user)
    return render_template('viewprofile.html', user=user)


"""



CREATE AND LIST ITEMS



"""

from myapp import myapp_obj
from myapp.forms import LoginForm, SignupForm, EditProfile, AgencySignupForm, ListingForm, VolunteerForm
from flask import render_template, flash, redirect, url_for
from flask import Flask

from myapp import db
from myapp.models import User, Profile, Listing, Volunteer
from flask_login import current_user, login_user, logout_user, login_required


def save_image(picture_file):
    picture_name = picture_file.filename
    picture_path = os.path.join(myapp_obj.root_path, 'static/listing_pics', picture_name)
    picture_file.save(picture_path)
    return picture_name

@myapp_obj.route("/createlisting", methods=['GET', 'POST'])
@login_required
def itemsForSale():
    form = ListingForm()
    user_id = current_user.id
    # a = User.query.with_entities(User.agency == 'True').all()
    a = User.query.filter(User.agency =='True').all()
    # form.agency.choices = [('0', 'None')] + a

    form.agency.choices = a
    a.insert(0,None)
	# form.agency.default = [('0', '-- select an option --')]


    if form.validate_on_submit():
        flash(f'Created!')
        name = form.name.data
        description = form.description.data
        location = int(form.location.data)
        agency = form.agency.data
        warehouse = form.warehouse.data
        free = form.free.data
        trade = form.trade.data
        image_file = save_image(form.picture.data)
        Listing.image_file = image_file
        listing = Listing(image_file, name, description, location, agency, warehouse, free, trade, user_id)
        if free is True:
            listing.set_price(0.00)
        elif trade is True:
            listing.set_price(0.00)
        else:
            listing.set_price(form.price.data)
        db.session.add(listing)
        db.session.commit()
        return redirect('/managelistings/'+ str(listing.id))
    # else:
    #     return redirect('/createerror')
    image_url = url_for('static', filename='listing_pics/'+ Listing.image_file)
    return render_template('listitem.html', a=a, form=form, image_url = image_url)

@myapp_obj.route("/createerror")
@login_required
def createerror():
	form = ListingForm()
	return render_template('createerror.html', form=form)

@myapp_obj.route("/createditem")
@login_required
def itemTest():
	item = Listing.query.get(listing_id)
    # form = Listing.query.all()
	return render_template('testfile.html', item=item)

@myapp_obj.route('/freelistings')
@login_required
def freelistings():
    sale = Listing.query.filter(Listing.free==True)
    title = "Free Listings"
    return render_template('listings.html', sale=sale, title=title)

@myapp_obj.route('/tradelistings')
@login_required
def tradelistings():
    sale = Listing.query.filter(Listing.trade==True)
    title = "Trade Listings"
    return render_template('listings.html', sale=sale, title=title)


@myapp_obj.route('/listings')
@login_required
def listings():
    sale = Listing.query.filter(Listing.free==False, Listing.trade==False)
    title = "Sale Listings"
    return render_template('listings.html', sale=sale, title=title)

@myapp_obj.route('/listings/<int:val>')
@login_required
def getListing(val):
    listing_id = val
    item = Listing.query.get(listing_id)
    items = []
    return render_template('testfile.html', items=items, item=item)

@myapp_obj.route('/freelistings/<int:val>')
@login_required
def free(val):
    listing_id = val
    item = Listing.query.get(listing_id)
    items = []
    return render_template('freeitem.html', items=items, item=item)

@myapp_obj.route('/getitfree/<int:val>')
@login_required
def getitfree(val):
    listing_id = val
    user_id = current_user.id
    listings = Listing.query.filter(Listing.user_id==user_id)
    count = Listing.query.filter(Listing.user_id==user_id).count()
    sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()

    item = Listing.query.get(listing_id)
    items = []
    return render_template('getitfree.html', items=items, item=item, count=count, sold=sold, listings= listings)

@myapp_obj.route('/bought/<int:val>')
@login_required
def bought(val):
	listing_id = val
	item = Listing.query.get(listing_id)
	name = item.name
	item.status="Sold"
	db.session.commit()
	return redirect(url_for('success', name=name))
	# return render_template('testfile.html', items=items, item=item)

@myapp_obj.route('/success/<string:name>')
@login_required
def success(name):
	user_id = current_user.id
	listings = Listing.query.filter(Listing.user_id==user_id)
	count = Listing.query.filter(Listing.user_id==user_id).count()
	sold = Listing.query.filter(Listing.user_id==user_id and Listing.status=='Sold').count()
	return render_template('success.html', name=name, listings=listings, sold=sold, count=count)


@myapp_obj.route('/managelistings/<int:val>')
@login_required
def manageListing(val):
    listing_id = val
    item = Listing.query.get(listing_id)

    return render_template('managelisting.html',  item=item)


@myapp_obj.route('/newname/<int:val>', methods=['GET', 'POST'])
def newName(val):
	item = Listing.query.get(val)
	form = NewName()
	value=val
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newname = form.name.data
		item.name = newname

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageListing', val=value))
	return render_template('newname.html', form=form, item=item, val=val)

@myapp_obj.route('/newprice/<int:val>', methods=['GET', 'POST'])
def newPrice(val):
	item = Listing.query.get(val)
	form = NewPrice()
	value=val
	if form.validate_on_submit():
		flash(f'Changes Saved!')
		newprice = form.price.data
		item.price = newprice

        # db.session.query(Listing).filter(
        # Listing.id == val).update({Listing.name: name})
		db.session.commit()
		return redirect(url_for('manageListing', val=value))
	return render_template('newprice.html', form=form, item=item, val=val)

@myapp_obj.route('/delete/<int:val>')
def deleteItem(val):
	item = Listing.query.get(val)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('listings'))
"""



VOLUNTEER




"""

@myapp_obj.route('/listvolunteer', methods=['GET', 'POST'])
@login_required
def listvolunteer():
    user_id = current_user.id
    form = VolunteerForm()
    if form.validate_on_submit():
        flash(f'Created!')
        name = form.name.data
        description = form.description.data
        location = form.location.data
        date = form.date.data
        vol = Volunteer(name, description, location, date, user_id)
        db.session.add(vol)
        db.session.commit()
        return redirect('/managevol/'+ str(vol.id))
    return render_template('listvolunteer.html', form=form)

@myapp_obj.route("/createdvol")
@login_required
def volTest():
    items = Volunteer.query.all()
    return render_template('testfile.html', items=items)

@myapp_obj.route('/vollisting')
@login_required
def vollistings():
    sale = Volunteer.query.all()
    title = "Volunteer Opportunities"
    return render_template('getvol.html', sale=sale, title=title)

@myapp_obj.route('/deletevol/<int:val>')
def deleteVol(val):
	item = Volunteer.query.get(val)
	db.session.delete(item)
	db.session.commit()
	return redirect(url_for('listings'))

@myapp_obj.route('/volsuccess/<int:val>')
def volsuccess(val):
    vol = Volunteer.query.get(val)
    return render_template('volsuccess.html', item=vol)



@myapp_obj.route('/volunteer')
@login_required
def volunteer():
    return render_template('VolunteerList.html')

@myapp_obj.route('/vollistings/<int:val>')
@login_required
def volListings(val):
    listing_id = val
    item = Volunteer.query.get(listing_id)
    items = []
    return render_template('vollistings.html', items=items, item=item)

@myapp_obj.route('/bevolunteer/<int:val>', methods=['GET', 'POST'])
@login_required
def bevolunteer(val):
    user = current_user.id
    print(user)
    vol_id = val
    bevol = BeVolunteer(user, vol_id)
    db.session.add(bevol)
    db.session.commit()
    # return redirect('/volsuccess')
    return redirect(url_for('volsuccess', val=val))

@myapp_obj.route('/managevol/<int:val>')
@login_required
def manageVol(val):
    listing_id = val
    item = Volunteer.query.get(listing_id)
    vols = BeVolunteer.query.filter(BeVolunteer.vol_id == listing_id).all()
    print(vols)
    a = []
    for i in vols:
        us = get_username(i.user_id)
        print(us)
        a.append(us)

    # for c,i in db.session.query(User, BeVolunteer).filter(User.bevolunteer == vols.user_id):
    #     user = get_username(c.id)
    #     a.append(c.get_username())

    return render_template('managevol.html',  item=item, vols=vols, a=a)

def get_username(user_id):
    user_id = user_id
    user = User.query.get(user_id)
    return user

"""



PAYMENTS



"""

YOUR_DOMAIN = 'http://127.0.0.1:5000'
stripe.api_key = 'sk_test_51KwJCGIVxGuZvYFf0YW5nfbMrKiW4fmwQZfpuOM1ai8b1y1CZb5OXKIFxbfGNhzW4DebQE2g7RC6ABu6Xq9NIC9D00eYLOFkSj'

@myapp_obj.route('/purchase/<int:val>', methods=['GET','POST'])
def create_checkout_session(val):
    item_id = val
    item = Listing.query.get(item_id)
    integer_price = int(item.price * 100)
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                  'price_data': {
                    'currency': 'usd',
                    'product_data': {
                      'name': item.name,
                    },
                    'unit_amount': integer_price,
                  },
                  'quantity': 1,
                }],
                mode='payment',
                success_url=YOUR_DOMAIN+ '/bought/'+str(val),
                cancel_url=YOUR_DOMAIN+ '/listings/'+str(val),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)
