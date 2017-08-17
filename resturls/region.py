import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.region import Region as Table


class Region(Base):
	table_name = 'tbl_region'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_region=None, is_active=None):
		""" Return all region information

		:param id_region: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_region is None and is_active is None:
				data = db.query(Table).all()
			elif id_region is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_region)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new region

		:param body: {
			code: INTEGER,
			name: JSON,
			id_state: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_state' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_state'")

		id_region = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		code = body['code'] if 'code' in body else None

		with Database() as db:
			db.insert(Table(id_region, id_language_content, body['id_state'], code))
			db.commit()

		return {
			'id_region': id_region,
			'message': 'region successfully created'
		}

	def modify(self, body):
		""" Modify a region

		:param body: {
			id_region: UUID,
			code: INTEGER,
			name: JSON,
			id_state: UUID,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_region' not in body:
			raise Exception("You need to pass a id_region")

		with Database() as db:
			data = db.query(Table).get(body['id_region'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'id_state' in body:
				data.id_state = body['id_state']
			if 'code' in body:
				data.code = body['code']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'region successfully modified'
		}

	def remove(self, id_region):
		""" Remove a region

		:param id_region: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_region)
			data.is_active = False
			db.commit()

		return {
			'message': 'region successfully removed'
		}