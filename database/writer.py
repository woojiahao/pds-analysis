import re

import pandas as pd
from numpy.core.multiarray import ndarray
from pandas import DataFrame
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists

from database.data_types import DataTypes


class Writer:
	def __init__(self, conn_str: str):
		self.conn_str = conn_str
		conn_str_valid = self.__verify_connection__()
		if not conn_str_valid[0]:
			raise Exception(conn_str_valid[1])

		if not database_exists(self.conn_str):
			raise Exception(f'Database: {self.conn_str[self.conn_str.rfind("/") + 1 : ]} does not exist')

		self.engine = create_engine(conn_str)
		self.Base = declarative_base(bind=self.engine)
		self.metadata = self.Base.metadata

	def write(self, tablename: str, data_frame: DataFrame, primary_keys: tuple = None, attrs: dict = None):
		if attrs is None and primary_keys is None:
			raise Exception('Specify the primary keys if you are not specifying the attributes')

		if self.__has_table__(tablename):
			raise Exception(f'{tablename} already exists in the database, please pick another table name')

		if attrs is not None:
			if '__tablename__' not in attrs:
				print(f'No __tablename__ attribute found, using the one supplied: {tablename}')
				attrs['__tablename__'] = tablename

			num_cols = data_frame.shape[1]
			if len(attrs) != num_cols + 1:
				raise Exception(
					f'Invalid number of columns, data frame requires {num_cols} columns, was given {len(attrs) - 1} columns')

			self.__check_attrs__(data_frame, attrs)

			data_frame = self.__match_attr__(data_frame, attrs)

			valid_pk, primary_keys = self.__is_valid_pk__(data_frame, attrs=attrs)
			if not valid_pk:
				raise Exception(f'Primary keys chosen for {attrs} is not valid')
		else:
			if not self.__is_valid_pk__(data_frame, primary_keys=primary_keys)[0]:
				raise Exception(f'Primary keys chosen {primary_keys} is not valid')

		data_frame, attr_dict = self.__generate_attr_dict__(tablename, data_frame, primary_keys, attrs)

		self.__create_table__(attr_dict)
		self.__populate_table__(data_frame, attr_dict['__tablename__'])

		print(f'Success: Created table: {tablename}')

	def __create_table__(self, attr_dict: dict):
		table = type(attr_dict['__tablename__'], (self.Base,), attr_dict)
		table.extend_existing = True
		self.metadata.create_all(self.engine)

	def __populate_table__(self, data_frame: DataFrame, tablename: str):
		self.metadata.reflect(bind=self.engine)
		table: Table = self.metadata.tables[tablename]
		with self.engine.connect() as conn:
			for row in data_frame.values:
				ins = table.insert(values=ndarray.tolist(row))
				conn.execute(ins)

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
				if column_name is '__tablename__':
					continue

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
							if column_name is not '__tablename__' and attributes['primary_key']]
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
			if column_name is '__tablename__':
				continue

			if column_name not in data_frame.columns:
				if 'backing' not in attributes:
					raise Exception(
						f'Specify a backing attribute if you are not using the default column name ({column_name}) in the data frame')

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
		"""
		for column_name, attributes in attrs.items():
			if column_name is '__tablename__':
				continue

			if 'dtype' not in attributes:
				raise Exception(f'Data type of column: {column_name} not specified')
			if 'primary_key' not in attributes:
				raise Exception(f'Primary key of column: {column_name} not specified')
			if column_name not in data_frame.columns and 'backing' not in attributes:
				raise Exception(f'Changing a column: {column_name} will require a \'backing\' field to be declared')

	def __has_table__(self, tablename: str):
		self.metadata.reflect(bind=self.engine)
		try:
			self.metadata.tables[tablename]
		except KeyError:
			return False
		return True

	def __verify_connection__(self) -> tuple:
		pattern = '^\w+:\/\/\w+:\w+\@\w+:\d+\/\w+$'
		if re.match(pattern, self.conn_str) is None:
			return False, 'Invalid format'

		return True, 'Valid'
