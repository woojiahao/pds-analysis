import re

from numpy.core.multiarray import ndarray
from pandas import DataFrame
from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists


class AlchemyManager:
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

	def has_table(self, tablename: str):
		self.metadata.reflect(bind=self.engine)
		try:
			self.metadata.tables[tablename]
		except KeyError:
			return False
		return True

	def create_table(self, attr_dict: dict):
		table = type(attr_dict['__tablename__'], (self.Base,), attr_dict)
		table.extend_existing = True
		self.metadata.create_all(self.engine)

	def populate_table(self, data_frame: DataFrame, tablename: str):
		self.metadata.reflect(bind=self.engine)
		table: Table = self.metadata.tables[tablename]
		with self.engine.connect() as conn:
			for row in data_frame.values:
				print(row)
				ins = table.insert(values=ndarray.tolist(row))
				conn.execute(ins)

	def __verify_connection__(self) -> tuple:
		pattern = '^\w+:\/\/\w+:\w+\@\w+:\d+\/\w+$'
		if re.match(pattern, self.conn_str) is None:
			return False, 'Invalid format'

		return True, 'Valid'
