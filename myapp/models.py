from myapp import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Boolean
from flask_login import UserMixin
from myapp import login


class User(UserMixin, db.Model):
    """
        This class represent for User table in database

        Attributes:
        ----------
        id: int (primary key)
        username: string
        email: string
        password: string
        to_do: object (foreign key)
        activities: Object (foreign key)
        flaskcard: Object (foreign key)

        Function:
        ---------
        __init__: constructor with 2 parameter username, email
        __repr__: representation a output
        set_password: auto generate password
        check_password: get and check password
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    admin = db.Column(db.String(10))
    agency = db.Column(db.String(10))
    profile = db.relationship('Profile', backref='users', lazy='dynamic')
    listings = db.relationship('Listing', backref='users', lazy='dynamic')
    volunteer = db.relationship('Volunteer', backref='users', lazy='dynamic')
    bevolunteer = db.relationship('BeVolunteer', backref='users', lazy='dynamic')

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    def __init__(self, username, email):
        self.username = username
        self.email = email
        

    def __repr__(self):
        return f'{self.username}'

    def set_time_login(self, timelogin):
        self.timelogin = timelogin

    def set_time_logout(self, timeloguot):
        self.timelogin = timeloguot

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def set_agency(self, agency):
        self.agency = agency

    def set_admin(self, admin):
        self.admin = admin

    def check_password(self, password):
        return check_password_hash(self.password, password)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String(64))
    last = db.Column(db.String(64))
    
    phone = db.Column(db.String(64))
    address1 = db.Column(db.String(128))
    address2 = db.Column(db.String(128))
    postal = db.Column(db.String(64))
    state = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def __init__(self , first, last, phone, address1, address2, postal, state, user_id):
        self.first = first
        self.last = last
        self.phone = phone
        self.address1 = address1
        self.address2 = address2
        self.postal = postal
        self.state = state
        self.user_id = user_id

# class Rating(db.Model):
#     __tablename__ = 'ratings'
#     id = db.Column(db.Integer, primary_key = True)
#     rating = db.Column(db.Float)
#     user_id


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    location = db.Column(db.String(5))
    agency = db.Column(db.String(128))
    warehouse = db.Column(db.String(5))
    free = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, default=0.00)
    trade = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String, default='For Sale')

    def __init__(self, name, description, location, agency, warehouse, free, trade, user_id):
        self.name = name
        self.description = description
        self.location = location
        self.agency = agency
        self.warehouse = warehouse
        self.free = free
        self.trade = trade
        self.user_id = user_id 

    def set_price(self, price):
        self.price = price

    def set_name(self, name):
        self.name = name 

    def set_desc(self, description):
        self.description = description

class Volunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    location = db.Column(db.String(5))
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vol = db.relationship('BeVolunteer', backref='volunteer', lazy='dynamic')

    def __init__(self, name, description, location, date, user_id):
        self.name = name
        self.description = description
        self.location = location
        self.date = date 
        self.user_id = user_id


class BeVolunteer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vol_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))

    def __init__(self, user_id, vol_id):
        self.user_id = user_id
        self.vol_id = vol_id


