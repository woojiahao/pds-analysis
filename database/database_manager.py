from config import Config
from database.data_types import DataTypes
from entities.entity import Entity
from entities.entity_loader import EntityLoader


class Manager:
	def __init__(self):
		print(Config.DATABASE_CONNECTION_STRING)
		self.entity_loader = EntityLoader()
		self.entities = []

	def load_data(self):
		self.__load_entities__()
		if not self.__has_database__():
			print('Data not loaded yet, loading now')
			self.entity_loader.add_entities(self.entities)
			self.entity_loader.load_all()
			print('Data loaded')

	def __has_database__(self) -> bool:
		has_table = True
		for entity in self.entities:
			has_table &= self.entity_loader.alchemy_manager.has_table(entity.tablename)

		return has_table

	def __load_entities__(self):
		live_births = Entity(
			tablename='live_births',
			file_name='data/live-births.csv',
			attrs={
				'year': {
					'dtype': DataTypes.INT64,
					'primary_key': True
				},
				'type': {
					'dtype': DataTypes.STR,
					'primary_key': True,
					'backing': 'level_1'
				},
				'total': {
					'dtype': DataTypes.INT64,
					'primary_key': False,
					'backing': 'value'
				}
			},
			replace_vals=['na'],
			fill_val=0
		)

		occupations = Entity(
			tablename='mothers_occupations',
			file_name='data/live-births-by-occupation-of-mother-and-birth-order.csv',
			attrs={
				'month': {
					'dtype': DataTypes.DATETIME,
					'primary_key': True
				},
				'occupation': {
					'dtype': DataTypes.STR,
					'primary_key': True,
					'backing': 'mother_occupation'
				},
				'order': {
					'dtype': DataTypes.STR,
					'primary_key': True
				},
				'birth_count': {
					'dtype': DataTypes.INT64,
					'primary_key': False,
				}
			}
		)

		enrolment = Entity(
			tablename='enrolment',
			file_name='data/primary-enrolment-by-age.csv',
			attrs={
				'year': {
					'dtype': DataTypes.INT64,
					'primary_key': True
				},
				'age': {
					'dtype': DataTypes.STR,
					'primary_key': True
				},
				'sex': {
					'dtype': DataTypes.STR,
					'size': 2,
					'primary_key': True
				},
				'enrolment': {
					'dtype': DataTypes.INT64,
					'primary_key': False,
					'backing': 'enrolment_primary'
				}
			}
		)

		gdp = Entity(
			tablename='gdp',
			file_name='data/gross-domestic-product-at-current-market-prices-annual.csv',
			attrs={
				'year': {
					'dtype': DataTypes.INT64,
					'primary_key': True
				},
				'misc': {
					'dtype': DataTypes.STR,
					'primary_key': False,
					'backing': 'level_1'
				},
				'total': {
					'dtype': DataTypes.FLOAT64,
					'primary_key': False,
					'backing': 'value'
				}
			}
		)

		self.entities.extend([enrolment, live_births, occupations, gdp])
