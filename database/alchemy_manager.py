from numpy.core.multiarray import ndarray
from pandas import DataFrame
from sqlalchemy import Table
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base

from app import db


class AlchemyManager:
	def __init__(self):
		self.engine: Engine = db.engine
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
		self.metadata.create_all(bind=self.engine)
		db.session.commit()
		print(f'{attr_dict["__tablename__"]} has been created')

	def populate_table(self, data_frame: DataFrame, tablename: str):
		self.metadata.reflect(bind=self.engine)
		table = self.metadata.tables[tablename]
		with self.engine.connect() as conn:
			for row in data_frame.values:
				print(row)
				ins = table.insert(values=ndarray.tolist(row))
				conn.execute(ins)
