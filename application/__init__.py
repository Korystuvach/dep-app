from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
# Initializing Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = b'5_#jlsv42;fsd]/2lf*#'
# Connect sqlite to flask object
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Turn on lodging all query to the database (SQL language). Turn off in production
app.config['SQLALCHEMY_ECHO'] = True
app.config['TESTING'] = True

# Create Instance for SQLAlchemy database
db = SQLAlchemy(app)

# Initialize login
login_manager = LoginManager()

# Initialize database migration
migrate = Migrate(app, db)

from application import models, routes
