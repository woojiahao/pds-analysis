from flask import Flask

from database.database_manager import Manager

app = Flask(__name__)
db_manager = Manager()

from app import routes