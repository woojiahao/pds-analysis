from app import app
from app import db
from database.database_manager import Manager
from plotting.plot_loader import PlotLoader


@app.shell_context_processor
def make_shell_context():
	return {
		'Manager': Manager,
		'engine': db.engine,
		'PlotLoader': PlotLoader
	}

if __name__ == '__main__':
	app.run(debug=True)