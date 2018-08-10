from app import app
from flask import render_template
from app import db_manager

@app.route('/')
@app.route('/index')
def index():
	db_manager.load_data()
	return render_template('base.html')
