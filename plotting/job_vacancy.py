import pygal

from plotting.custom_styles import style
from plotting.plot import Plot


class JobVacancy:
	def __init__(self, engine):
		self.engine = engine

	def plot_line_graph(self):
		data = self.query_data()
		line_graph = pygal.Line(
			show_legend=False,
			style=style,
			x_label_rotation=270,
			show_minor_x_labels=False)
		line_graph.title = 'Job Vacancy Rate'
		line_graph.x_labels = [key for key in data.keys()]
		line_graph.x_labels_major = [key for key in data.keys() if key[key.rfind('-') + 1:] == 'Q1']
		line_graph.add('Job Vacancy', [d for d in data.values()])
		line_graph.render_to_file(Plot.generate_plot_name('job_vacancy_rate'))

	def query_data(self):
		query = 'SELECT * FROM job_vacancy;'
		results = self.engine.execute(query)
		return { row['quarter']: row['job_vacancy_rate'] for row in results }