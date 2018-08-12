from flask import render_template, url_for

from app import app


@app.route('/')
@app.route('/home')
def home():
	return render_template(
		'home.html',
		page='Introduction',
		next=url_for('effects'))


@app.route('/effects')
def effects():
	return render_template(
		'effects.html',
		page='Effects of declining population',
		back=url_for('home'),
		next=url_for('hypothesis'))


@app.route('/hypothesis')
def hypothesis():
	return render_template(
		'hypothesis.html',
		page='Hypothesis',
		back=url_for('effects'),
		next=url_for('live_births_rate'))


@app.route('/live-births-rate')
def live_births_rate():
	return render_template(
		'live_births.html',
		page='Live Births Rate',
		back=url_for('hypothesis'),
		next=url_for('correlation_live_birth_enrolment'))


@app.route('/correlation_live_birth_enrolment')
def correlation_live_birth_enrolment():
	return render_template(
		'correlation_live_birth_enrolment.html',
		page='Correlation between live birth rate and primary enrolment',
		back=url_for('live_births_rate'),
		next=url_for('causes'))


@app.route('/causes')
def causes():
	return render_template(
		'causes.html',
		page='Potential causes of a declining population',
		back=url_for('correlation_live_birth_enrolment'),
		next=url_for('occupation')
	)


@app.route('/occupation')
def occupation():
	return render_template(
		'occupation.html',
		page='Mother\'s Occupation',
		back=url_for('causes'),
		next=url_for('cost_of_living'))


@app.route('/cost_of_living')
def cost_of_living():
	return render_template(
		'cost_of_living.html',
		page='Cost of living',
		back=url_for('occupation'))


@app.route('/setup')
def setup():
	return render_template('setup.html', page='Set-Up')


@app.route('/about')
def about():
	return render_template('about.html', page='About')
