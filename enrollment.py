import pandas as pd
import matplotlib.pyplot as plt

from database.data_types import DataTypes
from database.writer import Writer

file_name = 'data/primary-enrolment-by-age.csv'

db_writer = Writer('postgresql://postgres:root@localhost:5432/pds')
df = pd.read_csv(file_name)
"""
Ideal attr_dict structure:
key: column name
value: dictionary of attributes
+ dtype -> datatype
+ primary_key -> True/False (if not specified, false by defualt)
+ size -> Applicable for STR only
+ backing -> if the column name does not match up with the df column, refer to this field
"""
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
db_writer.write('temp', df, attrs=attr_dict)
