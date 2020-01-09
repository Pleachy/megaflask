import os

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
    
