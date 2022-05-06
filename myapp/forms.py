from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, FloatField, DateField
from wtforms.validators import (DataRequired, Email, EqualTo, Length, Optional)
from flask_wtf.file import FileField, FileRequired

class LoginForm(FlaskForm):
        """
    This class creates a user login form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    password (PasswordField): A single line of text for users to enter password
                    remember_me (BooleanField): a checkbox 
                    submit (SubmitField)

            Returns:
                    Show a login form
    """
        __tablename__ = 'users'
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember_me = BooleanField('Remember me', default=False)
        submit = SubmitField('Log In')

class SignupForm(FlaskForm):
        """
         This class creates a user signup form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    email (StringField): A single line of text for users to input email
                    password (PasswordField): A single line of text for users to enter password
                    confirm (PasswordFeild): A single line of text for users to re-enter password
                    submit (SubmitField)

            Returns:
                    Show a signup form
        """
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
        confirm = PasswordField('Confirm yor password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')


class AgencySignupForm(FlaskForm):
        """
         This class creates a user signup form

            Parameters:
                    username (StringField): A single line of text for user to input name
                    email (StringField): A single line of text for users to input email
                    password (PasswordField): A single line of text for users to enter password
                    confirm (PasswordFeild): A single line of text for users to re-enter password
                    submit (SubmitField)

            Returns:
                    Show a signup form
        """
        username = StringField('Username', validators=[DataRequired()])
        email = StringField('Email', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
        confirm = PasswordField('Confirm yor password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
        submit = SubmitField('Register')


class EditProfile(FlaskForm):
    first = StringField('First Name')
    last = StringField('Last Name')
    phone = StringField('Phone Number')
    address1 = StringField('Address Line 1')
    address2 = StringField('Address Line 2')
    postal = StringField('Postal Code')
    state = SelectField('State', choices = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'])
    submit = SubmitField('Save Changes')


class ListingForm(FlaskForm):
    name = StringField('Item Name')
    description = StringField('Item Description')
    location = StringField('Enter Postal Code')
    agency = SelectField('Enter Agency', choices=[])
    warehouse = BooleanField('Add Premium Warehouse?')
    free = BooleanField('List Item As Free')
    price = FloatField('Item Price (leave blank if free)', validators=[Optional()])
    trade = BooleanField('List Item For Trade')
    submit = SubmitField('Create Listing')


class VolunteerForm(FlaskForm):
    name = StringField('Volunteer Opportunity Name')
    description = StringField('Opportunity Description')
    location = StringField('Enter Postal Code')
    date = DateField('Enter Event Date', id='datepick', validators=[DataRequired()])
    submit = SubmitField('Create Opportunity')


class NewName(FlaskForm):
    name = StringField("Enter New Name")
    submit = SubmitField("Save Changes")

class NewDesc(FlaskForm):
    desc = StringField("Enter New Description")
    submit = SubmitField("Save Changes")

class NewPrice(FlaskForm):
    price = FloatField("Enter New Price")
    submit = SubmitField("Save Changes")
