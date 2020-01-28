from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5
import jwt
from app import app
from time import time

"""
Below is a direct translation of an association table between
users. We are not declaring this table as its own model since
this is an auxillary table with no data other than the foreign
keys.
"""
followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


# user class is inheriting from db.Model which is a base class
# for all models from Flask-SQLAlchemy.
# This class defines several fields as class variables and these fields
# are created as instances of the db.Column class which takes fild type
# as an argument along with other optional arguments.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    """
    like we did for the posts one to many relationship, we're using
    db.relationship to define the relationship in the model class.
    This relationship links User instances to other User instances
    so as a convention we're dgoing to say that for a pair of users
    linked by this relationship, the left side user is following
    the right side user.
    We're defining the rleationship as seen from the left side user
    with the name 'followed', because when we query this relationship
    from the left side, we will get a list of the followed users.
    """
    """
    - 'User' is the right side entity of the relationship (the left
    side entity is the parent class) since this is a self-referential
    relationship we have to use the same class on both sides.
    - 'secondary' configures the association table that is used
    for this relationship.
    - 'primaryjoin' indicaes the condition that links the left side
    entity(the follower user) with hte association table. The join
    condition for the left side of the relationship is the user ID
    matching the follower_id field of the association table. The
    followers.c.follower_id expression references the follower_id
    column of the association table.
    - 'secondaryjoin' indicates the condition that links the right
    side entity(the followed user) with the association table. This
    condition is similar to the one for primaryjoin, which the only
    difference that now we're using followed_id.
    - 'backref' defines how this relationship will be accessed from
    the right side entity. From the left side the relationship is named
    'followed' so from the right side we're going to use the name
    'followers' to represent all of the left side users that are linked
    to the target user in the right side. The addition of the 'lazy'
    argument indicates the execution mode for this query. A dynamic
    mode sets up the query to not run until specifically requested.
    - 'lazy' this one at the end applies to the left side side query
    instead of the right side.
    """
    followed = db.relationship(
        'User', secondary=followers,
        # why the == instead of =?
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # the posts field is not actually a database field, but a high-level
    # view of the relationship between users and posts and wont be
    # in the database diagram for that reason.
    # the db.relationship field is the 'one' in a one-to-many relationship
    #
    # The first argument to db.relationship is the model class representing
    # the 'many' side of the relationship. This argument can be provided as
    # a string with the class name if the model is defined later in the module
    #
    # Backref argument defines the name of a field added to the objects
    # of the 'many' class which points back at the 'one' object. It
    # will add a post.author expression that will return the user
    # given a post.
    #
    # The lazy argument defines how the database query for the
    # relationship will be issued.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # __repr__ method tells python how to print objects of this class
    # which is useful for debugging.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # with the two methods below in place, a user object can now do
    # secure password verification WITHOUT the need to ever store
    # original passwords.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    """
    this method of the User class returns the URL of the user's avatar image
    scaled to the requested size in pixels. For users without a registered
    avatar, an 'identicon' image will be geneerated. In order to generate the
    md5 hash, we convert the email to lowercase as is required by Gravatar.
    Then we encode the string as bytes since md5 support in Python only works
    on bytes.
    """
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp field is indexed which is useful for us since we will want
    # to retrieve the posts in chronological order.
    # a default argument was also added and passed datetime.utcnow.
    # when you pass a function as a default, SQLAlchemy will set the
    # field to the value of calling that function as a default. We also did
    # not include () ater utcnow, so we're passing the function itself
    # and not the result of calling it. In general we want to work with UTC
    # dates and times in a server application, ensuring that we use
    # uniform timestamps regardless of user location.
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post{}>'.format(self.body)

# the user loader is registered with Flask-Login usin gthe @login.user_loader
# decoartor. The id that Flask-Login passes to the function is going to be a
# string so databases that user numeric IDs need to convert the string
# to integer
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
