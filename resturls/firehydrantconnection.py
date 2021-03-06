import uuid
from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.fire_hydrant_connection import FireHydrantConnection as Table


class FireHydrantConnection(Base):
	table_name = 'tbl_fire_hydrant_connection'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant_connection=None, is_active=None):
		""" Return all information for fire hydrant connection

		:param id_fire_hydrant_connection: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant_connection is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant_connection is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant_connection)

		return {
			'data': data
		}


	def create(self, body):
		""" Create a new fire hydrant connection

		:param body: {
			id_fire_hydrant: UUID,
			diameter: FLOAT,
			id_unit_of_measure_diameter: UUID,
			id_fire_hydrant_connection_type: UUID,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_fire_hydrant' not in body:
			raise Exception("You need to pass a 'id_fire_hydrant'")

		id_fire_hydrant_connection = uuid.uuid4()
		diameter = body['diameter'] if 'diameter' in body else None
		id_unit_of_measure = body['id_unit_of_measure_diameter'] if 'id_unit_of_measure_diameter' in body else None
		id_fire_hydrant_connection_type = body['id_fire_hydrant_connection_type'] if 'id_fire_hydrant_connection_type' in body else None

		with Database() as db:
			db.insert(Table(id_fire_hydrant_connection_type, body['id_fire_hydrant'],
			                diameter, id_unit_of_measure, id_fire_hydrant_connection_type))
			db.commit()

		return {
			'id_fire_hydrant_connection': id_fire_hydrant_connection,
			'message': 'fire hydrant connection successfully created'
		}

	def modify(self, body):
		""" Modify a fire hydrant connection

		:param body: {
			id_fire_hydrant_connection: UUID,
			diameter: FLOAT,
			id_unit_of_measure_diameter: UUID,
			id_fire_hydrant_connection_type: UUID,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_fire_hydrant_connection' not in body:
			raise Exception("You need to pass a id_fire_hydrant_connection")

		with Database() as db:
			data = db.query(Table).get(body['id_fire_hydrant_connection'])

			if 'diameter' in body:
				data.diameter = body['diameter']
			if 'id_unit_of_measure_diameter' in body:
				data.id_unit_of_measure_diameter = body['id_unit_of_measure_diameter']
			if 'id_fire_hydrant_connection_type' in body:
				data.id_fire_hydrant_connection_type = body['id_fire_hydrant_connection_type']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'fire hydrant connection successfully modified'
		}

	def remove(self, id_fire_hydrant_connection):
		""" Remove a fire hydrant connection

		:param id_fire_hydrant_connection: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_fire_hydrant_connection)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire hydrant connection successfully removed'
		}