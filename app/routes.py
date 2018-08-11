from flask import render_template

from app import app
from app import db
from plotting.enrolment import Enrolment, Genders


# todo: render all the plots and save them, then use the saved plots instead of rendering everytime

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', page='Home')


@app.route('/about')
def about():
	return render_template('about.html', page='About')


@app.route('/effects')
def effects():
	enrolment = Enrolment(db.engine)
	return render_template(
		'effects.html',
		page='Effects',
		enrolment_line_male=enrolment.plot_line(Genders.MALE))
