from app import app, db
from database.database_manager import Manager
from plotting.plot_loader import PlotLoader


@app.shell_context_processor
def make_shell_context():
	return {
		'db_manager': Manager(),
		'plot_loader': PlotLoader(db.engine)
	}


if __name__ == '__main__':
	app.run(debug=True)
