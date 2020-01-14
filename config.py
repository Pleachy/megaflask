import os
basedir = os.path.abspath(os.path.dirname(__file__))

"""
the configuration settings are defined as class variables inside the config
class. As the application needs more configuration items they can be added to
this class, and if you need more than one configuration set then you can
create subclasses.
"""
class Config(object):
    """
    this secret key and its value are used by flask and some of its extensions
    as a cyptographic key (for generation of signatures or tokens) The Flask
    WTF extension uses it to protet web forms against Cross-Site Request
    Forgery(seasurf).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess-,-mortal'
    
    """
    Flask-SQLAlchemy extension takes the location of the application's
    database from the SQLAlCHEMY_DATABASE_URI configuration variable.
    as it is good practice, we provide a fallback value when the environment
    does not define the variable. Here i'm taking the database URL from
    the DATABASE_URL environment variable. if that is not denied then we 
    are configuring a database named app.db located in the main directory
    of the application, which is stored in the basedir vriable.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    """
    SQLALCHEMY_TRACK_MODIFICATIONS is set to flase to disable a feature
    which signals the appliation everytime a change is about to be made
    in the database.
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
