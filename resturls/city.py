import uuid

from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.city import City as Table


class City(Base):
	table_name = 'tbl_city'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_city=None, is_active=None):
		""" Return all city information

		:param id_city: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_city is None and is_active is None:
				data = db.query(Table).all()
			elif id_city is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_city)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new city

		:param body: {
			name: JSON,
			id_building: UUID,
			id_city_type: UUID,
			id_county: UUID,
			code: INTEGER,
			code3_letter: STRING,
			email_address: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_county' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_county'")

		id_city = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		id_building = body['id_building'] if 'id_building' in body else None
		id_city_type = body['id_city_type'] if 'id_city_type' in body else None
		code = body['code'] if 'code' in body else None
		code3_letter = body['code3_letter'] if 'code3_letter' in body else None
		email_address = body['email_address'] if 'email_address' in body else None

		with Database() as db:
			db.insert(Table(
				id_city, id_language_content, id_building, body['id_county'], id_city_type,
				code, code3_letter, email_address))
			db.commit()

		return {
			'id_city': id_city,
			'message': 'city successfully created'
		}

	def modify(self, body):
		""" Modify a city

		:param body: {
			id_city: UUID,
			id_county: UUID,
			id_building: UUID,
			name: JSON,
			code: INTEGER,
			code3_letter: STRING,
			email_address: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_city' not in body:
			raise Exception("You need to pass a id_city")

		with Database() as db:
			data = db.query(Table).get(body['id_city'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'id_building' in body:
				data.id_building = body['id_building']
			if 'id_city_type' in body:
				data.id_city_type = body['id_city_type']
			if 'id_county' in body:
				data.id_county = body['id_county']
			if 'code' in body:
				data.code = body['code']
			if 'code3_letter' in body:
				data.code3_letter = body['code3_letter']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'city successfully modified'
		}

	def remove(self, id_city):
		""" Remove a city

		:param id_city: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_city)
			data.is_active = False
			db.commit()

		return {
			'message': 'city successfully removed'
		}