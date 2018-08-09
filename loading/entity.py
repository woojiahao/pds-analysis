import numpy as np
import pandas as pd

from database.writer import Writer


class Entity:
	def __init__(self, tablename: str, file_name: str, attrs: dict = None, primary_keys: list = None,
				 replace_vals: list = None, fill_val: object = None):
		self.file_name = file_name
		self.tablename = tablename
		self.replace_vals = replace_vals
		self.fill_val = fill_val
		self.primary_keys = primary_keys
		self.attrs = attrs

	def set_writer(self, writer: Writer):
		self.writer = writer

	def load(self):
		df = pd.read_csv(self.file_name)
		if self.replace_vals is not None:
			if self.fill_val is None:
				raise Exception(f'Specify a fill value for replacing: {self.replace_vals}')
			else:
				df = df.replace(self.replace_vals, np.NaN).fillna(self.fill_val)

		self.writer.write(self.tablename, df, primary_keys=self.primary_keys, attrs=self.attrs)
