from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from database.database_manager import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_CONNECTION_STRING
db = SQLAlchemy(app)
manager = Manager()

from app import routes
