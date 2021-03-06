import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.construction_type import ConstructionType as Table


class ConstructionType(Base):
	table_name = 'tbl_construction_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_construction_type=None, is_active=None):
		""" Return all information for construction type

		:param id_construction_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_construction_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_construction_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_construction_type)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new construction type

		:param body: {
			name: JSON,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'name' not in body:
			raise Exception("You need to pass a 'name'")

		id_construction_type = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)

		with Database() as db:
			db.insert(Table(id_construction_type, id_language_content))
			db.commit()

		return {
			'id_construction_type': id_construction_type,
			'message': 'construction type successfully created'
		}

	def modify(self, body):
		""" Modify a construction type

		:param body: {
			id_construction_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_construction_type' not in body:
			raise Exception("You need to pass a id_construction_type")

		with Database() as db:
			data = db.query(Table).get(body['id_construction_type'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'construction type successfully modified'
		}

	def remove(self, id_construction_type):
		""" Remove a construction type

		:param id_construction_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_construction_type)
			data.is_active = False
			db.commit()

		return {
			'message': 'construction type successfully removed'
		}