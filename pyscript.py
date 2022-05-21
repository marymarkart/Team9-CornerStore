import myapp
from myapp.models import User, Listing
from myapp import db

user = User('admin','adminemail1@cornerstore.com')
user.set_password('Security1')
user.set_admin('True')
db.session.add(user)


agency = User('Default Agency','thisistheagency@cornerstore.com')
agency.set_password('password')
agency.set_agency('True')
agency.set_verified('True')
db.session.add(agency)


agency = User('Test Charity','thisisthecharity@cornerstore.com')
agency.set_password('password')
agency.set_agency('True')
agency.set_verified('False')
db.session.add(agency)

tester = User('Bob','thisistester@cornerstore.com')
tester.set_password('password')
db.session.add(tester)

tester1 = User('Alice','thisistester1@cornerstore.com')
tester1.set_password('password')
db.session.add(tester1)

listing1 = Listing('laptop.jpg', 'Mac Pro Laptop 2016', 'This laptop works but needs a new battery', '95125', 'None', False, False, False, 4)
listing1.set_price(145.45)
db.session.add(listing1)

listing2 = Listing('Grand-Piano.jpg', 'Grand Piano', "This piano was a gift but I don't have room for it", '95125', 'None', False, True, False, 4)
db.session.add(listing2)

listing3 = Listing('placeholder-image.png', 'Placeholder Card', "This is a placeholder card to use a a placeholder, I want to trade it for an actual picture", '95125', 'None', False, False, True, 4)
db.session.add(listing3)

db.session.commit()
