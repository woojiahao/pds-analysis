from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from plotting.enrolment import Enrolment, Genders

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = Config.DATABASE_CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

enrolment = Enrolment(db.engine)
enrolment.plot_line_graph(Genders.MALE)
enrolment.plot_line_graph(Genders.FEMALE)
enrolment.plot_line_graph(Genders.BOTH)

from app import routes
