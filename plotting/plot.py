from sqlalchemy.engine import Engine


class Plot:
	@staticmethod
	def generate_plot_name(plot_name: str):
		return f'app/static/images/plots/{plot_name}.svg'

	@staticmethod
	def get_year_range(engine: Engine, year_col: str, table_name: str):
		query = f'SELECT MIN(DISTINCT({year_col})) AS "min_year", MAX(DISTINCT({year_col})) AS "max_year" from {table_name};'
		result = engine.execute(query)
		years = { }
		for row in result:
			years['min'] = row[0]
			years['max'] = row[1]
		return years
