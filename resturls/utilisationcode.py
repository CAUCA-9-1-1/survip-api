import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.utilisation_code import UtilisationCode as Table


class UtilisationCode(Base):
	table_name = 'tbl_utilisation_code'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_utilisation_code=None, is_active=None):
		""" Return all information for utilisation code

		:param id_utilisation_code: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_utilisation_code is None and is_active is None:
				data = db.query(Table).all()
			elif id_utilisation_code is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_utilisation_code)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new utilisation code

		:param body: {
			name: JSON,
			cubf: STRING,
			scian: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'cubf' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'cubf'")

		id_utilisation_code = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		scian = body['scian'] if 'scian' in body else None

		with Database() as db:
			db.insert(Table(id_utilisation_code, id_language_content, body['cubf'], scian))
			db.commit()

		return {
			'id_utilisation_code': id_utilisation_code,
			'message': 'utilisation code successfully created'
		}

	def modify(self, body):
		""" Modify a utilisation code

		:param body: {
			id_utilisation_code: UUID,
			name: JSON,
			cubf: STRING,
			scian: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_utilisation_code' not in body:
			raise Exception("You need to pass a id_utilisation_code")

		with Database() as db:
			data = db.query(Table).get(body['id_utilisation_code'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'cubf' in body:
				data.cubf = body['cubf']
			if 'scian' in body:
				data.scian = body['scian']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'utilisation code successfully modified'
		}

	def remove(self, id_utilisation_code):
		""" Remove a utilisation code

		:param id_utilisation_code: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_utilisation_code)
			data.is_active = False
			db.commit()

		return {
			'message': 'utilisation code successfully removed'
		}