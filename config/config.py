import os
from config import local_db_url

class Config:
	DATABASE_CONNECTION_STRING = os.getenv('DATABASE_URL') or local_db_url