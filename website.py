from app import app
from database.database_manager import Manager


@app.shell_context_processor
def make_shell_context():
	return {
		'Manager': Manager
	}

if __name__ == '__main__':
	app.run(debug=True)