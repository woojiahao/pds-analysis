import re

from pandas import DataFrame
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists


# todo: add checking of what is in the attr_dict to ensure that it conforms to the desired standards
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

	def write(self, tablename: str, data_frame: DataFrame, primary_keys: tuple = None, attr_dict: dict = None):
		if attr_dict is None and primary_keys is None:
			raise Exception('Specify the primary keys if you are not specifying the attributes')

		if self.__has_table__(tablename):
			raise Exception(f'{tablename} already exists in the database, please pick another table name')

		if attr_dict is not None:
			if '__tablename__' not in attr_dict.keys():
				print(f'No __tablename__ attribute found, using the one supplied: {tablename}')
				attr_dict['__tablename__'] = tablename

			num_cols = data_frame.shape[1]
			if len(attr_dict) != num_cols + 1:
				raise Exception(
					f'Invalid number of columns, data frame requires {num_cols} columns, was given {len(attr_dict) - 1} columns')

			data_frame = self.__match_attr__(data_frame, attr_dict)

			if not self.__is_valid_pk__(data_frame, attr_dict=attr_dict):
				raise Exception(f'Primary keys chosen for {attr_dict} is not valid')
		else:
			if not self.__is_valid_pk__(data_frame, primary_keys):
				raise Exception(f'Primary keys chosen {primary_keys} is not valid')

			attr_dict = self.__generate_attr_dict__(tablename, data_frame, primary_keys)

	def __generate_attr_dict__(self, tablename: str, data_frame: DataFrame, primary_keys: tuple) -> dict:
		attr_dict = { '__tablename__': tablename }
		dtypes = data_frame.dtypes

		for column_name, data_type in dtypes.items():
			pass

		return attr_dict

	def __is_valid_pk__(self, data_frame: DataFrame, primary_keys: tuple = None, attr_dict: dict = None) -> bool:
		if primary_keys is None:
			primary_keys = [column_name for column_name, attributes in attr_dict.items()
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

		return len(filtered) == len(set(filtered))


	def __match_attr__(self, data_frame: DataFrame, attr_dict: dict) -> DataFrame:
		col_names = { }
		for column_name, attributes in attr_dict.items():
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
