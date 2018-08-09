import pandas as pd

from database.data_types import DataTypes
from database.writer import Writer

file_name = 'data/gross-domestic-product-at-current-market-prices-annual.csv'

db_writer = Writer('postgresql://postgres:root@localhost:5432/pds')
df = pd.read_csv(file_name)

attr_dict = {
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
db_writer.write('gdp', df, attrs=attr_dict)
