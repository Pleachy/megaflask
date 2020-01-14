from app import app, db
from app.models import User, Post

#this decorator registers the function as a shell context function.
#when the flask shell command runs it will invoke this function and
#register the items returned by it in the shell session.
#The reason the function returns a dictionary and not a list is because
#for each item you have to also provide a name under which it will
#be referenced in the shell, which is given by dictionary keys.
@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, 'Post': Post}

