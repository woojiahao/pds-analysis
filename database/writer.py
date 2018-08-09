import re

from pandas import DataFrame
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists


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

		print('Initialized!')

	def write(self, tablename: str, data_frame: DataFrame, attr_dict: dict = None):
		if attr_dict is not None:
			if '__tablename__' not in attr_dict.keys():
				print(f'No __tablename__ attribute found, using the one supplied: {tablename}')
				attr_dict['__tablename__'] = tablename

			num_cols = data_frame.shape[1]
			if len(attr_dict) != num_cols + 1:
				raise Exception(f'Invalid number of columns, data frame requires {num_cols} columns, was given {len(attr_dict) - 1} columns')

		print('Writing!')

	def __verify_connection__(self) -> tuple:
		pattern = '^\w+:\/\/\w+:\w+\@\w+:\d+\/\w+$'
		if re.match(pattern, self.conn_str) is None:
			return False, 'Invalid format'

		return True, 'Valid'
