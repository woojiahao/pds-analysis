from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return 'Hello world'
