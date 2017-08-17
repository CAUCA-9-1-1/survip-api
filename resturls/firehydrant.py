import uuid
from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.fire_hydrant import FireHydrant as Table


class FireHydrant(Base):
	table_name = 'tbl_fire_hydrant'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_hydrant=None, is_active=None):
		""" Return all information for fire hydrant

		:param id_fire_hydrant: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_hydrant is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_hydrant is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_hydrant)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new fire hydrant

		:param body: {
			id_fire_hydrant_type: JSON,
			id_lane: UUID,
			id_intersection: UUID,
			altitude: FLOAT,
			fire_hydrant_number: STRING,
			id_operator_type_rate: UUID,
			rate_from: STRING,
			rate_to: STRING,
			id_unit_of_measure_rate: UUID,
			id_operator_type_pressure: UUID,
			pressure_from: STRING,
			pressure_to: STRING,
			id_unit_of_measure_pressure: UUID,
			color: STRING,
			comments: STRING,
			physical_position: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_fire_hydrant_type' not in body or 'fire_hydrant_number' not in body:
			raise Exception("You need to pass a 'fire_hydrant_number' and 'id_fire_hydrant_type'")

		id_fire_hydrant = uuid.uuid4()
		id_lane = body['id_lane'] if 'id_lane' in body else None
		id_intersection = body['id_intersection'] if 'id_intersection' in body else None

		with Database() as db:
			db.insert(Table(id_fire_hydrant, body['id_fire_hydrant_type'], body['fire_hydrant_number'],
			                id_lane, id_intersection))
			db.commit()

		return {
			'id_fire_hydrant': id_fire_hydrant,
			'message': 'fire hydrant successfully created'
		}

	def modify(self, body):
		""" Modify a fire hydrant

		:param body: {
			id_fire_hydrant_type: JSON,
			id_lane: UUID,
			id_intersection: UUID,
			altitude: FLOAT,
			fire_hydrant_number: STRING,
			id_operator_type_rate: UUID,
			rate_from: STRING,
			rate_to: STRING,
			id_unit_of_measure_rate: UUID,
			id_operator_type_pressure: UUID,
			pressure_from: STRING,
			pressure_to: STRING,
			id_unit_of_measure_pressure: UUID,
			color: STRING,
			comments: STRING,
			physical_position: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_fire_hydrant' not in body:
			raise Exception("You need to pass a id_fire_hydrant")

		with Database() as db:
			data = db.query(Table).get(body['id_fire_hydrant'])

			if 'id_fire_hydrant_type' in body:
				data.id_fire_hydrant_type = body['id_fire_hydrant_type']
			if 'fire_hydrant_number' in body:
				data.fire_hydrant_number = body['fire_hydrant_number']
			if 'id_lane' in body:
				data.id_lane = body['id_lane']
			if 'id_intersection' in body:
				data.id_intersection = body['id_intersection']
			if 'altitude' in body:
				data.altitude = body['altitude']
			if 'id_operator_type_rate' in body:
				data.id_operator_type_rate = body['id_operator_type_rate']
			if 'from_rate' in body:
				data.from_rate = body['from_rate']
			if 'to_rate' in body:
				data.to_rate = body['to_rate']
			if 'id_unit_of_measure_rate' in body:
				data.id_unit_of_measure_rate = body['id_unit_of_measure_rate']
			if 'id_operator_type_pressure' in body:
				data.id_operator_type_pressure = body['id_operator_type_pressure']
			if 'from_pressure' in body:
				data.from_pressure = body['from_pressure']
			if 'to_pressure' in body:
				data.to_pressure = body['to_pressure']
			if 'id_unit_of_measure_pressure' in body:
				data.id_unit_of_measure_pressure = body['id_unit_of_measure_pressure']
			if 'color' in body:
				data.color = body['color']
			if 'comments' in body:
				data.comments = body['comments']
			if 'physical_position' in body:
				data.physical_position = body['physical_position']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'fire hydrant successfully modified'
		}

	def remove(self, id_fire_hydrant):
		""" Remove a fire hydrant

		:param id_fire_hydrant: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_fire_hydrant)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire hydrant successfully removed'
		}