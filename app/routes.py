from app import app, manager
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')
