import pandas as pd

from database.data_types import DataTypes
from database.writer import Writer

file_name = 'data/primary-enrolment-by-age.csv'

db_writer = Writer('postgresql://postgres:root@localhost:5432/pds')
df = pd.read_csv(file_name)

attr_dict = {
	'__tablename__': 'temp',
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
db_writer.write('enrolment', df, attrs=attr_dict)
