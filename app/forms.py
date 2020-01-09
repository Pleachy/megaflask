#most flask extensions use a flask_<name> naming convention for top level
#import symbol. FLask-WTF has all its symbols under flask_wtf and is where
#FlaskForm is imported from.
from flask_wtf import FlaskForm
#these four classes representing the field types are imported directly from 
#the WTForms package.
#For each field an object is created as a class variable in the LoginForm
#class, and each field is given a description or label as a first argument.
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	#the optional validators argument is used to attach validation behavior
	#to fields.
	#DataRequired validator hcecks that the field is not submitted empty
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

