from flask import render_template

from app import app


@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html', page='Home')


@app.route('/about')
def about():
	return render_template('about.html', page='About')
