from flask import render_template

from app import app
from app import db
from plotting.enrolment import Enrolment, Genders


@app.route('/')
@app.route('/home')
@app.route('/analysis')
def home():
	enrolment = Enrolment(db.engine)
	return render_template(
		'home.html',
		page='Home',
		enrolment_line_male=enrolment.plot_line(Genders.MALE))


@app.route('/about')
def about():
	return render_template('about.html', page='About')
