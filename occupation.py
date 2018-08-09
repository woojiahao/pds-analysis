import pandas as pd

from database.data_types import DataTypes
from database.writer import Writer

file_name = 'data/live-births-by-occupation-of-mother-and-birth-order.csv'

db_writer = Writer('postgresql://postgres:root@localhost:5432/pds')
df = pd.read_csv(file_name)

attr_dict = {
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
db_writer.write('mothers_occupations', df, attrs=attr_dict)
