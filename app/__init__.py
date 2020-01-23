# from python module 'module name' import 'class'
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
# db object which represents the databse
db = SQLAlchemy(app)
# migrate is an object representing
migrate = Migrate(app, db)
login = LoginManager(app)
# the 'login' value is the function(or endpoint) name for the login
# view; the name you would use in a url_for() call to get the URL
login.login_view = 'login'

from app import routes, models, errors
"""
we only enable the email logger when the application is running
without debug mode. Which is indicated by app.debug being True, and also
when the email server exists in the configuration.
In essence the code below creates a SMPTHandler instance, sets its
level so that it only reports errors and not warnings, informational, or
debugging messages, and lastly attaches it to the app.logger object
from flask.
"""
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure :(',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    """
    The RotatingFileHandler class, as one might assume, rotates the logs which
    ensures that the log files do not grow too large when the app has been
    running for a long time. We've limited the size of the log file to 10kb,
    and are keeping the last 10 logs files as backup.
    The logging.Formatter class provides custom formatting for the log messages
    Since these messages are going to a file we want them to have as much
    information as possible. So we're using a format that includes the
    timestamp, the logging level, the message and the source file line and
    number from where the log entry originated.
    To make the logging more useful we're also lowering the logging level to
    the INFO category. The categories in ascending order if importance are:
    DEBUG, INFO, WARNING, ERROR and CRITICAL.
    The server also writes a line to the logs each time it starts. When
    the application runs on a production server these log entires will tell
    you when the server was
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
