from flask import render_template, flash, redirect, url_for, request
from app import app, db
#imports LoginForm class from forms.py
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from flask_login import logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

#decorators for the index method
@app.route('/')
@app.route('/index')
#the way Flask_Login protects a view function against anonymous
#users is with a decorator called @login_required. When you add this
#decorator below the @app.route decorators from Flask, the function
#becomes protected and will not allow access to users that are not
#authenticated.
@login_required
def index():
    
    posts = [
        {
            'author': {'username': 'Twudge'},
            'body': 'Another beautiful day in Pudge Town!'
        },
        {
            'author': {'username': 'Zeddius'},
            'body': 'Just finished casting my first snowball spell!'
        },
        {
            'author': {'username': 'Ronnoc'},
            'body': 'Twice blast and confound those damnable ragamuffins! If one more of those weasels makes it into my pantry I swear on the nine i will teleport it straight to Murkmill!'
            
        }
    ]
    #return render_template('index.html', title='Home', user=user)
    return render_template('index.html', titel='Home Page', posts=posts)

#the methods argument in the route decorator tells Flask that this
#view function accepts GET and POST requests, overriding the default 
#which is to only accept GET requests
#(HTTP protocl states that GET requests are those that return information
#to the client, the we browser in this case).
#POST requests are typically used when the browser submits form data to 
#to the server(GET can also do this but its not a reccomended practice)
@app.route('/login', methods=['GET', 'POST'])
def login():

    #these two lines deal with a funky situation, if you have a user
    #thats already logged in, and tries to navigate back to the login 
    #screen. clearly thats a mistake so we're gonna say, no, and not
    #allow that to happen by firmly redirecting the user.
    #The current_user vairable comes from Flask-Login and can be used
    #any time during the handling to obtain the user object that
    #represents the client of the request. The value of this variable 
    #can be a user object from the database.
    #
    #is_authenticated is one of the properties we gave our user
    #class by importing UserMixin which checks to see if the user
    #is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    #instantiating an object from the LoginForm class and
    #sent it down to the template.
    form = LoginForm()
    #form.validate_ons_submit method does all the form processing work.
    #When the browser sends the GET requests to recieve the web page form,
    #this method will return False and the program will skip to the second
    #return statement to render the template.
    #
    #When the browser sends POST as a result of the user pressing the submit
    #button, form.validate_on_submit will gather all the data, run all of the
    #validators attached to the fields and if everything is correct will 
    #return True.
    #
    #When it returns true, the login view functions calls two functions
    #imported from Flask. flash() which is useful for showing a message
    #to the user. The second function is redirect() which instructs the
    #client web browser to automatically navigate to a different page,
    #given as an argument.
    if form.validate_on_submit():
        #we are using filter_by() to load the user from the database.
        #the form submission requires a username so thats what we will
        #query the databse with.
        #The result of filter_by() is a query that only includes the 
        #objects that have a matching username. Since we know that there
        #is only going to be one or zero results, we complete the query
        #by calling first(). which will return the user object if it
        #exists, or None if it does not.
        user = User.query.filter_by(username=form.username.data).first()
        #here we use the check_password function from Flask-Login
        #and flash a message if the password is wrong, or doesn't exist
        #for the given username.
        if user is None or not user.check_password(form.password.data):
            #when flash is called, flask stores the message, but we have
            #to make some changes to our base.html file to render the 
            #message in a way that works for the site layout.
            flash('invalid username or password :(')
            return redirect(url_for('login'))
        #the login_user() function will register the user as logged in
        #so that any future pages the user navigates to will have
        #the current_user variable set to that user.
        login_user(user, remember=form.remember_me.data)
        #right after the user is logged in by calling login_user(), 
        #the value of the next query string argument is obtained.
        #Flask provides a request variable containing the information
        #that the client sent with the request.
        next_page = request.args.get('next')
        """
        There are three possible cases that need to be considered to 
        determine where to redirect after a successful login:
        - If the login URl does not have a next argument, then the
        user is redirected to the index page
        - If the login URl includes a next argument that is set to a 
        relative path(a URl without the domain prtion) then the user
        is redirected to that URL.
        - If the login URL includes a next argument that is set to a
        full URL that includes a domain name, then the user is
        redirected to the index page.
        The third case is in place to make the application more secure
        An attacker could insert a URL to a malicious site in the 'next'
        argument so the application only redirects when the URL is relative,
        ensuring that the redirect stays within the same application.
        To determine if the URL is relative or absolute, we use Werkzeug's
        url_parse() and check if the netloc component is set or not.
        """
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    #form=form is simply passing the form object created in the line
    #above to the template with the name 'form'
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! And welcome to our humble home.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)









