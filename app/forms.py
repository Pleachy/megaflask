# most flask extensions use a flask_<name> naming convention for top level
# import symbol. FLask-WTF has all its symbols under flask_wtf and is where
# FlaskForm is imported from.
from flask_wtf import FlaskForm
# these four classes representing the field types are imported directly from
# the WTForms package.
# For each field an object is created as a class variable in the LoginForm
# class, and each field is given a description or label as a first argument.
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from wtforms.validators import Length
from app.models import User


class LoginForm(FlaskForm):
    # the optional validators argument is used to attach validation behavior
    # to fields.
    # DataRequired validator hcecks that the field is not submitted empty
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    # The second validator 'Email' is a stock validator that comes with
    # WTForms that ensures what the user types matches the structure
    # of an email address
    email = StringField('Email', validators=[DataRequired(), Email()])
    # we ask for two passwords to prevent typos
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    """
    We've added two methods to this class, when you add any methods
    that match the pattern 'validate_<field_name>', WTForms takes
    those as custom validators and invokes them in addition to the
    stock validators. In this case we are making sure that the username
    and email are not already in the database so these two methods
    issue database queries expecting no results. If there are results
    then we tirgger a validation error by raising 'ValidationError'. The
    message included as the argument in the exception will be displayed
    to the user next to the appropriate field.
    """
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email address is already in use.')


class EditProfileForm(FlaskForm):
    """
    we have a new field type and validator in this form. A TextAreaField which
    is a multiline box in which the user can enter text. To validate this field
    we use 'Length' which will make sure that our text is betwen 0 and 140
    characters.
    """
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    """
    The implementation is in a custom validation method, but there
    is an overloaded constructor which accepts the original
    username as an argument. This uername is saved as an insance
    variable and then checked in the validate_username() method.
    If the username entered in the form is the same as the
    original username then there is no reason to check the
    database for duplicates
    """
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
