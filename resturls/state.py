import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.state import State as Table


class State(Base):
	table_name = 'tbl_state'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_state=None, is_active=None):
		""" Return all state information

		:param id_state: UUID
		:param id_active: BOOLEAN
		"""
		with Database() as db:
			if id_state is None and is_active is None:
				data = db.query(Table).all()
			elif id_state is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_state)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new state

		:param args: {
			name: JSON,
			id_country: UUID,
			ansi_code: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_country' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_country'")

		id_state = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		ansi_code = body['ansi_code'] if 'ansi_code' in body else None

		with Database() as db:
			db.insert(Table(id_state, id_language_content, body['id_country'], ansi_code))
			db.commit()

		return {
			'id_state': id_state,
			'message': 'state successfully created'
		}

	def modify(self, body):
		""" Modify a state

		:param body: {
			id_state: UUID,
			name: JSON,
			id_country: UUID,
			ansi_code: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_state' not in body:
			raise Exception("You need to pass a id_state")

		with Database() as db:
			data = db.query(Table).get(body['id_state'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])

			if 'id_country' in body:
				data.id_country = body['id_country']
			if 'ansi_code' in body:
				data.ansi_code = body['ansi_code']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'state successfully modified'
		}

	def remove(self, id_state):
		""" Remove a state

		:param id_state: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_state)
			data.is_active = False
			db.commit()

		return {
			'message': 'state successfully removed'
		}