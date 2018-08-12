import collections
import pygal

from plotting.custom_styles import style
from plotting.plot import Plot


class Jobs:
	UNCLASSIFIED = 'WKRS NOT CLASSIFIABLE BY OCCUPATION'
	PROFESSIONAL = 'PROFESSIONALS'
	UNEMPLOYED = 'PERSONS NOT ECONOMICALLY ACTIVE'
	TECHNICIANS = 'TECHNICIANS & ASSOCIATE PROFS'
	PRODUCTION = 'PRODUCTION CRAFTSMEN & REL WORKERS'
	LEGISLATORS = 'LEGISLATORS, SNR OFFICIALS & MGRS'
	CLEANERS = 'CLEANERS, LABOURERS & REL WORKERS'
	CLERKS = 'CLERICAL WORKERS'
	FARMERS = 'AGRICULTURAL & FISHERY WORKERS'
	RETAIL = 'SERVICE WKRS, SHOP, MARKET SALES WKRS'
	FACTORY = 'PLANT/MACHINE OPERATORS & ASSEMBLERS'


class Occupation:
	def __init__(self, engine):
		self.engine = engine

	def plot_line_graph(self):
		data = self.query_collection_data()
		line_graph = pygal.Line(x_label_rotation=270, style=style)
		line_graph.title = 'Live births by Working and Non-Working women'
		line_graph.add('Working', [dist['working'] for dist in data.values()])
		line_graph.add('Non-Working', [dist['non_working'] for dist in data.values()])
		line_graph.x_labels = [str(key) for key in data.keys()]
		line_graph.render_to_file(Plot.generate_plot_name('working_non_working_live_births'))

	def plot_bar_graph(self):
		data = self.query_distribution_data()
		bar_graph = pygal.Bar(
			show_legend=False,
			x_label_rotation=270,
			style=style,
			truncate_label=max(map(len, list(data.keys()))))
		bar_graph.title = 'Live Births By Mother\'s Occupation'
		bar_graph.x_labels = [key for key in data.keys()]
		bar_graph.add('Live Births', [val for val in data.values()])
		bar_graph.render_to_file(Plot.generate_plot_name('occupation_bar'))

	def query_collection_data(self):
		data = { }
		query = 'select working.month, working.working_bc as "Working", nonworking.nonworking_bc as "Non Working" ' \
				'from (select month, sum(birth_count) as working_bc from mothers_occupations where occupation not in (\'PERSONS NOT ECONOMICALLY ACTIVE\', \'WKRS NOT CLASSIFIABLE BY OCCUPATION\') group by month order by month) as working,' \
				'(select month, sum(birth_count) as nonworking_bc from mothers_occupations where occupation in (\'PERSONS NOT ECONOMICALLY ACTIVE\', \'WKRS NOT CLASSIFIABLE BY OCCUPATION\') group by month order by month) as nonworking ' \
				'where working.month = nonworking.month ' \
				'order by working.month;'
		results = self.engine.execute(query)
		for row in results:
			month = str(row['month'])
			data[month[:month.rfind('-')]] = {
				'working': row['Working'],
				'non_working': row['Non Working']
			}
		return data

	def query_distribution_data(self):
		query = 'SELECT occupation, SUM(birth_count) ' \
				'FROM mothers_occupations ' \
				'GROUP BY occupation ' \
				'ORDER BY occupation;'
		result = self.engine.execute(query)
		return { row['occupation']: row['sum'] for row in result }
