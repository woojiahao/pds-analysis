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

	def plot_histogram(self, job, year):
		interval = 50

		data = self.query_occupation_data(job, year)
		filtered = self.filter(data, interval)
		histogram = pygal.Histogram(
			show_legend=False,
			style=style
		)
		histogram.title = f'Distribution of live births - {job} in {year}'
		intervals = [int(key) for key in filtered.keys()]
		histogram.x_labels = intervals
		histogram.add(f'{job}', self.create_values(self.filter(data, interval), interval))
		histogram.render_to_file(Plot.generate_plot_name(f'occupation_histogram_{job}_{year}'))

	def create_values(self, data, interval):
		return [(len(value), int(key), int(key) + interval) for key, value in data.items()]

	def filter(self, data, interval):
		filtered = collections.OrderedDict()
		lower_lim, upper_lim = self.find_limit(
			list(sorted(data.values()))[0],
			list(sorted(data.values()))[len(data) - 1],
			interval
		)
		for i in range(lower_lim, upper_lim + 1, interval):
			filtered[str(i)] = []
			for value in data.values():
				if i <= value < i + 50:
					filtered[str(i)].append(value)

		return filtered

	def find_limit(self, lower, upper, interval):
		lower_copy, lower_counter = self.break_up(lower)
		upper_copy, upper_counter = self.break_up(upper)

		lower_lim = int(lower_copy) * pow(10, lower_counter)
		while lower_lim + interval < lower:
			lower_lim += interval

		upper_lim = int(upper_copy) * pow(10, upper_counter)
		while True:
			upper_lim += interval
			if upper_lim > upper:
				break

		return lower_lim, upper_lim

	def break_up(self, val):
		counter = 0
		copy = val
		while copy > 10:
			copy /= 10
			counter += 1
		return copy, counter

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

	def query_occupation_data(self, job, year):
		query = 'SELECT month, SUM(birth_count) ' \
				'FROM mothers_occupations ' \
				f'WHERE occupation = \'{job}\' AND date_part(\'year\', month) = {year} ' \
				'GROUP BY month ' \
				'ORDER BY month;'
		result = self.engine.execute(query)
		return { row['month']: row['sum'] for row in result }

	def query_distribution_data(self):
		query = 'SELECT occupation, SUM(birth_count) ' \
				'FROM mothers_occupations ' \
				'GROUP BY occupation ' \
				'ORDER BY occupation;'
		result = self.engine.execute(query)
		return { row['occupation']: row['sum'] for row in result }
