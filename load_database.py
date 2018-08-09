from config import Config
from database.data_types import DataTypes
from entities.entity import Entity
from entities.entity_loader import EntityLoader

entity_loader = EntityLoader(Config.DATABASE_CONNECTION_STRING)

live_births = Entity(
	tablename='live_births',
	file_name='data/live-births.csv',
	attrs={
		'__tablename__': 'live_births',
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
		'__tablename__': 'mothers_occupations',
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
		'__tablename__': 'enrolment',
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
		'__tablename__': 'gdp',
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

entity_loader.add_entities([enrolment, live_births, occupations, gdp])
entity_loader.load_all()
