import re

from pandas import DataFrame
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


class Writer:
	def __init__(self, conn_str: str):
		self.conn_str = conn_str
		conn_str_valid = self.__verify_connection__()
		if not conn_str_valid[0]:
			raise Exception(conn_str_valid[1])

		self.engine = create_engine(conn_str)
		self.Base = declarative_base(bind=self.engine)
		self.metadata = self.Base.metadata

	def __verify_connection__(self):
		pattern = '^\w+:\/\/\w+:\w+\@\w+:\d+\/\w+$'
		if re.match(pattern, self.conn_str) is None:
			return False, 'Invalid format'

		return True, 'Valid'
