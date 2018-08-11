import numpy as np
import pygal as pygal
from sqlalchemy.engine import Engine

from plotting.custom_styles import style
from plotting.plot import Plot


class Genders:
	MALE = {
		'title': 'Male',
		'value': 'MF'
	}
	FEMALE = {
		'title': 'Female',
		'value': 'F'
	}
	BOTH = {
		'title': 'Both'
	}


class Enrolment:
	def __init__(self, engine: Engine):
		self.engine = engine
		self.age_group = [
			'UNDER 7 YRS', '7 YRS', '8 YRS', '9 YRS', '10 YRS',
			'11 YRS', '12 YRS', '13 YRS', '14 YRS & OVER'
		]
		self.year_range = Plot.get_year_range(self.engine, 'year', 'enrolment')

	@staticmethod
	def generate_title(gender):
		return f'Primary Enrolment {gender["title"]} - By Age'

	def plot_line_graph(self, gender):
		line_chart = pygal.Line(x_label_rotation=270, style=style)
		line_chart.title = self.generate_title(gender)
		line_chart.x_labels = map(str, np.arange(self.year_range['min'], self.year_range['max'] + 1))
		ages = self.query_data(gender)
		for age, data in ages.items():
			line_chart.add(age, data)

		line_chart.render_to_file(Plot.generate_plot_name(f'enrolment_{gender["title"].lower()}'))

	def query_data(self, gender):
		ages = { }
		for age in self.age_group:
			ages[age] = []

			if gender == Genders.BOTH:
				query = f'SELECT year, age, sum(enrolment.enrolment) AS enrolment FROM enrolment WHERE age=\'{age}\' GROUP BY year, age ORDER BY year;'
			else:
				query = f'SELECT * FROM enrolment WHERE sex=\'{gender["value"]}\' AND age=\'{age}\';'

			result = self.engine.execute(query)
			for row in result:
				ages[age].append(row['enrolment'])
		return ages