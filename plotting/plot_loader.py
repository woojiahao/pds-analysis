from plotting.enrolment import Enrolment, Genders
from plotting.enrolment_live_birth import EnrolmentLiveBirth
from plotting.job_vacancy import JobVacancy
from plotting.live_birth_rates import LiveBirthRate
from plotting.occupation import Occupation
from plotting.resale_price import ResalePrice, FlatType


class PlotLoader():
	def __init__(self, engine):
		self.engine = engine

	def load_plots(self):
		enrolment = Enrolment(self.engine)
		enrolment.plot_line_graph(Genders.MALE)
		enrolment.plot_line_graph(Genders.FEMALE)
		enrolment.plot_line_graph(Genders.BOTH)

		live_births = LiveBirthRate(self.engine)
		live_births.plot_line_graph()
		live_births.plot_bar_graph()

		correlation = EnrolmentLiveBirth(self.engine)
		correlation.plot_wrong_scatter()
		correlation.plot_right_scatter()

		occupation = Occupation(self.engine)
		occupation.plot_line_graph()
		occupation.plot_bar_graph()

		job_vacancy = JobVacancy(self.engine)
		job_vacancy.plot_line_graph()

		resale_price = ResalePrice(self.engine)
		resale_price.plot_histogram(FlatType.FOUR_ROOM, 2015)
		resale_price.plot_box_plot([FlatType.THREE_ROOM, FlatType.FOUR_ROOM, FlatType.FIVE_ROOM, FlatType.EXECUTIVE], 1)
		resale_price.plot_line_graph([FlatType.THREE_ROOM, FlatType.FOUR_ROOM, FlatType.FIVE_ROOM, FlatType.EXECUTIVE])
