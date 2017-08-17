import uuid

from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.county import County as Table


class County(Base):
	table_name = 'tbl_county'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_county=None, is_active=None):
		""" Return all county information

		:param id_county: UUID
		:param id_active: BOOLEAN
		"""
		with Database() as db:
			if id_county is None and is_active is None:
				data = db.query(Table).all()
			elif id_county is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_county)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new county

		:param body: {
			name: JSON,
			id_state: UUID,
			id_region: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_state' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_state'")

		id_county = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		id_region = body['id_region'] if 'id_region' in body else None

		with Database() as db:
			db.insert(Table(id_county, id_language_content, body['id_state'], id_region))
			db.commit()

		return {
			'id_county': id_county,
			'message': 'county successfully created'
		}

	def modify(self, body):
		""" Modify a county

		:param body: {
			id_county: UUID,
			name: JSON,
			id_state: UUID,
			id_region: UUID
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_county' not in body:
			raise Exception("You need to pass a id_county")

		with Database() as db:
			data = db.query(Table).get(body['id_county'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'id_state' in body:
				data.id_state = body['id_state']
			if 'id_region' in body:
				data.id_region = body['id_region']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'county successfully modified'
		}

	def remove(self, id_county):
		""" Remove a county

		:param id_county: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_county)
			data.is_active = False
			db.commit()

		return {
			'message': 'county successfully removed'
		}