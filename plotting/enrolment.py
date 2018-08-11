import numpy as np
import pygal as pygal
from sqlalchemy.engine import Engine

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


class Enrolment:
	def __init__(self, engine: Engine):
		self.engine = engine
		self.age_group = [
			'UNDER 7 YRS', '7 YRS', '8 YRS', '9 YRS', '10 YRS',
			'11 YRS', '12 YRS', '13 YRS', '14 YRS & OVER'
		]

	@staticmethod
	def generate_title(gender):
		return f'Primary Enrolment {gender["title"]} - By Age'

	def plot_line(self, gender):
		line_chart = pygal.Line(x_label_rotation=270)
		line_chart.title = self.generate_title(gender)
		year_range = self.get_year_range()
		line_chart.x_labels = map(str, np.arange(year_range['min'], year_range['max']))
		ages = self.query_ages(gender)
		for age, data in ages.items():
			line_chart.add(age, data)
		return line_chart
		# line_chart.render_to_file(Plot.generate_plot_name(f'enrolment_{gender["title"]}'))

	def query_ages(self, gender):
		ages = { }
		for age in self.age_group:
			ages[age] = []
			query = f'SELECT * FROM enrolment WHERE sex=\'{gender["value"]}\' AND age=\'{age}\';'
			result = self.engine.execute(query)
			for row in result:
				ages[age].append(row['enrolment'])
		return ages

	def get_year_range(self):
		query = 'SELECT MIN(DISTINCT(year)) AS "min_year", MAX(DISTINCT(year)) AS "max_year" from enrolment;'
		result = self.engine.execute(query)
		years = { }
		for row in result:
			years['min'] = row[0]
			years['max'] = row[1]
		return years
