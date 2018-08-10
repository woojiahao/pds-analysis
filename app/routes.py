from app import app, manager
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	manager.load_data()
	return render_template('base.html')
