from flask import render_template

from app import app


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', page='Introduction')


@app.route('/effects')
def effects():
	return render_template('effects.html', page='Effects of declining population')


@app.route('/hypothesis')
def hypothesis():
	return render_template('hypothesis.html', page='Hypothesis')


@app.route('/live-births-rate')
def live_births_rate():
	return render_template('live_births.html', page='Live Births Rate')


@app.route('/correlation_live_birth_enrolment')
def correlation_live_birth_enrolment():
	return render_template(
		'correlation_live_birth_enrolment.html',
		page='Correlation between live birth rate and primary enrolment')


@app.route('/setup')
def setup():
	return render_template('setup.html', page='Set-Up')


@app.route('/about')
def about():
	return render_template('about.html', page='About')
