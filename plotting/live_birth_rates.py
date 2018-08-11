import numpy as np
import pygal

from plotting.custom_styles import style
from plotting.plot import Plot


class LiveBirthRate:
	def __init__(self, engine):
		self.engine = engine
		self.year_range = Plot.get_year_range(self.engine, 'year', 'live_births')

	def plot_line_graph(self):
		line_chart = pygal.Line(show_legend=False, x_label_rotation=270, style=style)
		line_chart.title = 'Live Births'
		line_chart.x_labels = map(str, np.arange(self.year_range['min'], self.year_range['max'] + 1))
		line_chart.add('Live Births', self.query_data())
		line_chart.render_to_file(Plot.generate_plot_name('live_birth_line'))

	def query_data(self):
		query = 'SELECT * FROM live_births WHERE type=\'Total Live-births\';'
		result = self.engine.execute(query)
		return [row['total'] for row in result]