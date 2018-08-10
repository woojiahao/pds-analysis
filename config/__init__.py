from json import load

with open('config.json') as file:
	data = load(file)

local_db_url = data['local_database_url']
print(local_db_url)