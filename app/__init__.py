#from python module 'module name' import 'class'
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
#db object which represents the databse
db = SQLAlchemy(app)
#migrate is an object representing 
migrate = Migrate(app, db)

#models is a module which will help us define the structure
#of the database
from app import routes, models
