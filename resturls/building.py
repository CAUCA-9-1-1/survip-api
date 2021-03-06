import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.building import BuildingFull as Table


class Building(Base):
	table_name = 'tbl_building'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building=None, is_active=None):
		""" Return all building information

		:param id_building: UUID
		:param is_active: Boolean
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			if id_building is None:
				if is_active is None:
					data = db.query(Table).all()
				else:
					data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_building)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new building

		:param body: {
			name: JSON,
			id_lane: UUID
			civic_number: STRING
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		id_building = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)

		with Database() as db:
			db.insert(Table(id_building, id_language_content, body['civic_number']))
			db.commit()

		return {
			'id_building': id_building,
			'message': 'building successfully created'
		}

	def modify(self, body):
		""" Modify all information for building

		:param body: {
			id_building: UUID,
			name: JSON,
			civic_number: STRING
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_building' not in body:
			raise Exception("You need to pass a id_building")

		with Database() as db:
			data = db.query(Table).get(body['id_building'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'civic_number' in body:
				data.civic_number = body['civic_number']
			if 'year_of_construction' in body:
				data.year_of_construction = body['year_of_construction']
			if 'building_value' in body:
				data.building_value = body['building_value']
			if 'number_of_floors' in body:
				data.number_of_floors = body['number_of_floors']
			if 'number_of_appartment' in body:
				data.number_of_appartment = body['number_of_appartment']

			db.commit()

		return {
			'message': 'building successfully modified'
		}

	def remove(self, id_building):
		""" Remove building

		:param id_building: UUID
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_building)
			data.is_active = False
			db.commit()

		return {
			'message': 'building successfully removed'
		}