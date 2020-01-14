from datetime import datetime
from app import db

#user class is inheriting from db.Model which is a base class
#for all models from Flask-SQLAlchemy.
#This class defines several fields as class variables and these fields
#are created as instances of the db.Column class which takes fild type
#as an argument along with other optional arguments.
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	#the posts field is not actually a database field, but a high-level
	#view of the relationship between users and posts and wont be 
	#in the database diagram for that reason.
	#the db.relationship field is the 'one' in a one-to-many relationship
    #
	#The first argument to db.relationship is the model class representing
	#the 'many' side of the relationship. This argument can be provided as 
	#a string with the class name if the model is defined later in the module
    #
	#Backref argument defines the name of a field added to the objects
	#of the 'many' class which points back at the 'one' object. It
	#will add a post.author expression that will return the user
	#given a post.
	#
	#The lazy argument defines how the database query for the 
	#relationship will be issued.
	posts = db.relationship('Post', backref='author', lazy='dynamic')

    #__repr__ method tells python how to print objects of this class
    #which is useful for debugging.
	def __repr__(self):
		return '<User {}>'.format(self.username)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	#timestamp field is indexed which is useful for us since we will want
	#to retrieve the posts in chronological order.
	#a default argument was also added and passed datetime.utcnow.
	#when you pass a function as a default, SQLAlchemy will set the 
	#field to the value of calling that function as a default. We also did
	#not include () ater utcnow, so we're passing the function itself
	#and not the result of calling it. In general we want to work with UTC
	#dates and times in a server application, ensuring that we use
	#uniform timestamps regardless of user location.
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post{}>'.format(self.body)


