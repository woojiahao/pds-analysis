import collections
import pygal

from plotting.custom_styles import style
from plotting.plot import Plot


class FlatType:
	ONE_ROOM = '1-room'
	TWO_ROOM = '2-room'
	THREE_ROOM = '3-room'
	FOUR_ROOM = '4-room'
	FIVE_ROOM = '5-room'
	EXECUTIVE = 'Executive'


class ResalePrice:
	def __init__(self, engine):
		self.engine = engine
		self.quarters = self.get_quarters()

	def plot_histogram(self, flat_type, year):
		interval = 50000

		data = self.query_price_data(flat_type, year)
		print(data)

		filtered = self.filter(data, interval)
		histogram = pygal.Histogram(
			show_legend=False,
			style=style,
			x_label_rotation=270
		)
		histogram.title = f'Distribution of resale price - {flat_type} in {year}'
		histogram.x_labels = [int(key) for key in filtered.keys()]
		histogram.add(f'{flat_type}', self.create_values(self.filter(data, interval), interval))
		histogram.render_to_file(Plot.generate_plot_name(f'resale_price_distribution_{flat_type}_{year}'))

	def plot_box_plot(self, flats, quarter):
		data = self.query_distribution_data(flats, quarter)

		box_plot = pygal.Box(box_mode="stdev", style=style)
		box_plot.title = f'Distribution of median resale prices in the Q{quarter} (All Time)'
		box_plot.x_labels = flats
		for flat in flats:
			box_plot.add(flat, data[flat])

		box_plot.render_to_file(Plot.generate_plot_name(f'resale_price_distribution_box_Q{quarter}_all_time'))

	def plot_line_graph(self, flats):
		data = self.query_trend_data(flats)
		line_graph = pygal.Line(
			style=style,
			x_label_rotation=270
		)
		line_graph.x_labels = self.quarters
		line_graph.title = 'Trend of resale prices (All time)'
		for flat in flats:
			line_graph.add(flat, data[flat])
		line_graph.render_to_file(Plot.generate_plot_name('resale_price_trend'))

	def query_trend_data(self, flats):
		data = collections.OrderedDict()
		for flat in flats:
			query = f'SELECT quarter, SUM(price) ' \
					f'FROM resale_price ' \
					f'WHERE flat_type = \'{flat}\' ' \
					f'GROUP BY quarter ' \
					f'ORDER BY quarter;'
			results = self.engine.execute(query)
			data[flat] = [row['sum'] for row in results]

		return data

	def query_distribution_data(self, flats, quarter):
		data = { }
		for flat in flats:
			query = f'SELECT price FROM resale_price WHERE flat_type=\'{flat}\' AND quarter like \'%%Q{quarter}\''
			results = self.engine.execute(query)
			data[flat] = sorted([row['price'] for row in results if row['price'] > 0])

		return data

	def query_price_data(self, flat_type, year):
		query = f'SELECT * FROM resale_price WHERE quarter LIKE \'{year}%%\' AND flat_type=\'{flat_type}\';'
		results = self.engine.execute(query)
		return sorted([row['price'] for row in results if row['price'] > 0])

	def get_quarters(self):
		query = 'SELECT DISTINCT quarter FROM resale_price ORDER BY quarter;'
		results = self.engine.execute(query)
		return [row['quarter'] for row in results]

	def create_values(self, data, interval):
		return [(len(value), int(key), int(key) + interval) for key, value in data.items()]

	def filter(self, data, interval):
		filtered = collections.OrderedDict()
		lower_lim, upper_lim = self.find_limit(data[0], data[len(data) - 1], interval)
		for i in range(lower_lim, upper_lim + 1, interval):
			filtered[str(i)] = [value for value in data if i <= value < i + interval]

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
