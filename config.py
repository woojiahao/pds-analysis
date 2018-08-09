import os

class Config:
	DATABASE_CONNECTION_STRING = os.getenv('DATABASE_URL') or 'postgresql://postgres:root@localhost:5432/pds'