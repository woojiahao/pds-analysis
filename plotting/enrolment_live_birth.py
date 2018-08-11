import pygal

from plotting.custom_styles import style
from plotting.plot import Plot


class EnrolmentLiveBirth:
	def __init__(self, engine):
		self.engine = engine

	def plot_wrong_scatter(self):
		scatter_plot = pygal.XY(
			stroke=False,
			style=style,
			show_legend=False,
			x_title='Live Birth Rate',
			y_title='Primary Enrolment')
		scatter_plot.title = 'Correlation between Primary Enrolment and Live Birth Rate'
		scatter_plot.add('Correlation', self.query_data('wrong'))
		scatter_plot.render_to_file(Plot.generate_plot_name('correlation_enrolment_live_birth_wrong'))

	def plot_right_scatter(self):
		scatter_plot = pygal.XY(
			stroke=False,
			style=style,
			show_legend=False,
			x_title='Live Birth Rate',
			y_title='Primary Enrolment')
		scatter_plot.title = 'Correlation between Primary Enrolment and Live Birth Rate'
		scatter_plot.add('Correlation', self.query_data('right'))
		scatter_plot.render_to_file(Plot.generate_plot_name('correlation_enrolment_live_birth_right'))

	def query_data(self, version):
		if version == 'wrong':
			query = 'SELECT e.year, lb.total, SUM(e.enrolment) ' \
					'FROM enrolment AS e, live_births AS lb ' \
					'WHERE e.year = lb.year AND lb.type=\'Total Live-births\' ' \
					'GROUP BY e.year, lb.total ' \
					'ORDER BY year;'
		else:
			query = 'SELECT e.year, lb.total, SUM(e.enrolment) ' \
					'FROM enrolment AS e, live_births AS lb ' \
					'WHERE e.year = lb.year + 6 AND lb.type=\'Total Live-births\' ' \
					'GROUP BY e.year, lb.total ' \
					'ORDER BY year;'

		print(query)
		result = self.engine.execute(query)
		return [(row['total'], row['sum']) for row in result]
