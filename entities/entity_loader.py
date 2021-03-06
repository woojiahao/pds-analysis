from database.alchemy_manager import AlchemyManager
from database.writer import Writer
from entities.entity import Entity


class EntityLoader:
	def __init__(self):
		self.entities = None
		self.alchemy_manager = AlchemyManager()
		self.writer = Writer(self.alchemy_manager)

	def add_entity(self, entity: Entity):
		if self.entities is None:
			self.entities = []

		entity.set_writer(self.writer)
		self.entities.append(entity)

	def add_entities(self, entities: list):
		if self.entities is None:
			self.entities = []

		for entity in entities:
			self.add_entity(entity)

	def load_all(self):
		for entity in self.entities:
			entity.load()
