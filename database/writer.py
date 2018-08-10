import pandas as pd
from pandas import DataFrame
from sqlalchemy import *

from database.alchemy_manager import AlchemyManager
from database.data_types import DataTypes


# todo: introduce more date formats
class Writer:
	def __init__(self, alchemy_manager: AlchemyManager):
		self.alchemy_manager = alchemy_manager

	def write(self, tablename: str, data_frame: DataFrame, primary_keys: tuple = None, attrs: dict = None):
		if attrs is None and primary_keys is None:
			raise Exception('Specify the primary keys if you are not specifying the attributes')

		if self.alchemy_manager.has_table(tablename):
			raise Exception(f'{tablename} already exists in the database, please pick another table name')

		if attrs is not None:
			num_cols = data_frame.shape[1]
			if len(attrs) != num_cols:
				raise Exception(
					f'Invalid number of columns, data frame requires {num_cols} columns, was given {len(attrs)} columns')

			self.__check_attrs__(data_frame, attrs)

			data_frame = self.__match_attr__(data_frame, attrs)

			valid_pk, primary_keys = self.__is_valid_pk__(data_frame, attrs=attrs)
			if not valid_pk:
				raise Exception(f'Primary keys chosen for {attrs} is not valid')
		else:
			if not self.__is_valid_pk__(data_frame, primary_keys=primary_keys)[0]:
				raise Exception(f'Primary keys chosen {primary_keys} is not valid')

		data_frame, attr_dict = self.__generate_attr_dict__(tablename, data_frame, primary_keys, attrs)

		self.alchemy_manager.create_table(attr_dict)
		self.alchemy_manager.populate_table(data_frame, attr_dict['__tablename__'])

		print(f'Success: Created table: {tablename}')

	def __generate_attr_dict__(self, tablename: str, data_frame: DataFrame, primary_keys: tuple,
							   attrs: dict = None) -> tuple:
		attr_dict = { '__tablename__': tablename }

		if attrs is None:
			for columm_name, data_type in data_frame.dtypes.items():
				dtype = None
				if data_type == DataTypes.INT64:
					dtype = Integer
				elif data_type == DataTypes.STR:
					dtype = String(data_frame[columm_name].map(len).max())
				elif data_type == DataTypes.BOOLEAN:
					dtype = Boolean
				elif data_type == DataTypes.DATETIME:
					dtype = Date
				elif data_type == DataTypes.FLOAT64:
					dtype = Float

				attr_dict[columm_name] = Column(dtype, primary_key=columm_name in primary_keys)
		else:
			for column_name, attributes in attrs.items():
				dtype = None
				data_type = attributes['dtype']
				if data_type == DataTypes.INT64:
					data_frame[column_name] = pd.to_numeric(data_frame[column_name], downcast='integer')
					dtype = Integer
				elif data_type == DataTypes.STR:
					data_frame[column_name] = data_frame[column_name].astype(str)
					max_length = data_frame[column_name].map(len).max()
					dtype = String(max_length if 'size' not in attributes else attributes['size'])
				elif data_type == DataTypes.FLOAT64:
					data_frame[column_name] = pd.to_numeric(data_frame[column_name], downcast='float')
					dtype = Float
				elif data_type == DataTypes.DATETIME:
					data_frame[column_name] = pd.to_datetime(data_frame[column_name])
					dtype = Date
				elif data_type == DataTypes.BOOLEAN:
					data_frame[column_name] = data_frame[column_name].astype(bool)
					dtype = Boolean

				attr_dict[column_name] = Column(dtype, primary_key=attributes['primary_key'])

		return data_frame, attr_dict

	def __is_valid_pk__(self, data_frame: DataFrame, primary_keys: tuple = None, attrs: dict = None) -> tuple:
		if primary_keys is None:
			primary_keys = [column_name for column_name, attributes in attrs.items()
							if attributes['primary_key']]
		else:
			for primary_key in primary_keys:
				if primary_key not in data_frame.columns:
					raise Exception(f'Primary key: {primary_key} is not a valid column name')

		if len(primary_keys) == 0:
			raise Exception('No primary keys selected')

		filtered = data_frame[primary_keys[0]].map(str)

		for i in range(1, len(primary_keys)):
			filtered += data_frame[primary_keys[i]].map(str)

		return len(filtered) == len(set(filtered)), primary_keys

	def __match_attr__(self, data_frame: DataFrame, attrs: dict) -> DataFrame:
		col_names = { }
		for column_name, attributes in attrs.items():
			if column_name not in data_frame.columns:
				col_names[attributes['backing']] = column_name
			else:
				col_names[column_name] = column_name

		return data_frame.rename(columns=col_names)

	def __check_attrs__(self, data_frame: DataFrame, attrs: dict):
		"""
		Ideal attr_dict structure:
		key: column name
		value: dictionary of attributes
		+ dtype -> datatype
		+ primary_key -> True/False
		+ size -> Applicable for STR only
		+ backing -> if the column name does not match up with the df column, refer to this field

		Sample:
		attrs = {
			'year': {
				'dtype': DataTypes.INT64,
				'primary_key': True
			},
			'cost': {
				'dtype': DataTypes.FLOAT64,
				'primary_key': False,
				'backing': 'value'
			}
		}
		"""
		for column_name, attributes in attrs.items():
			if 'dtype' not in attributes:
				raise Exception(f'Data type of column: {column_name} not specified')
			if 'primary_key' not in attributes:
				raise Exception(f'Primary key of column: {column_name} not specified')
			if column_name not in data_frame.columns and 'backing' not in attributes:
				raise Exception(f'Changing a column: {column_name} will require a \'backing\' field to be declared')
