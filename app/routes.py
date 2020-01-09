from flask import render_template, flash, redirect, url_for
from app import app
#imports LoginForm class from forms.py
from app.forms import LoginForm

#decorators for the index method
@app.route('/')
@app.route('/index')
def index():
    user = {'username': "Pleachy"}
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
    return render_template('index.html', user=user, posts=posts)

#the methods argument in the route decorator tells Flask that this
#view function accepts GET and POST requests, overriding the default 
#which is to only accept GET requests
#(HTTP protocl states that GET requests are those that return information
#to the client, the we browser in this case).
#POST requests are typically used when the browser submits form data to 
#to the server(GET can also do this but its not a reccomended practice)
@app.route('/login', methods=['GET', 'POST'])
def login():
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
        #when flash is called, flask stores the message, but we have
        #to make some changes to our base.html file to render the 
        #message in a way that works for the site layout.
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    #form=form is simply passing the form object created in the line
    #above to the template with the name 'form'
    return render_template('login.html', title='Sign In', form=form)
