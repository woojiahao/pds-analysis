import pandas as pd
import numpy as np

from database.data_types import DataTypes
from database.writer import Writer

file_name = 'data/live-births.csv'

db_writer = Writer('postgresql://postgres:root@localhost:5432/pds')
df = pd.read_csv(file_name).replace('na', np.NaN).fillna(0)

attr_dict = {
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
}
db_writer.write('live_births', df, attrs=attr_dict)
