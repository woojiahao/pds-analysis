import pygal
from flask import render_template, url_for

from app import app
from app import db
from plotting.enrolment import Enrolment, Genders

# todo: render all the plots and save them, then use the saved plots instead of rendering everytime

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

@app.route('/processing/<switch>')
def processing(switch):
	enrolment = Enrolment(db.engine)
	if switch == 'MALE':
		return enrolment.plot_line(Genders.MALE).render_data_uri()
	elif switch == 'FEMALE':
		return enrolment.plot_line(Genders.FEMALE).render_data_uri()

