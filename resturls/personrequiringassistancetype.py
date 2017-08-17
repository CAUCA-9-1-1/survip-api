import uuid

from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.person_requiring_assistance_type import PersonRequiringAssistanceType as Table


class PersonRequiringAssistanceType(Base):
	table_name = 'tbl_person_requiring_assistance_type'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_person_requiring_assistance_type=None, is_active=None):
		""" Return all person requiring assistance type information

		:param person_requiring_assistance_type: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_person_requiring_assistance_type is None and is_active is None:
				data = db.query(Table).all()
			elif id_person_requiring_assistance_type is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_person_requiring_assistance_type)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new person requiring assistance type

		:param body: {
			name: JSON,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'name' not in body:
			raise Exception("You need to pass a 'name'")

		id_person_requiring_assistance_type = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)

		with Database() as db:
			db.insert(Table(id_person_requiring_assistance_type, id_language_content))
			db.commit()

		return {
			'id_person_requiring_assistance_type': id_person_requiring_assistance_type,
			'message': 'person requiring assistance type successfully created'
		}

	def modify(self, body):
		""" Modify a person requiring assistance type

		:param body: {
			id_person_requiring_assistance_type: UUID,
			name: JSON,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_person_requiring_assistance_type' not in body:
			raise Exception("You need to pass a id_person_requiring_assistance_type")

		with Database() as db:
			data = db.query(Table).get(body['id_person_requiring_assistance_type'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'person requiring assistance type successfully modified'
		}

	def remove(self, id_person_requiring_assistance_type):
		""" Remove a person requiring assistance type

		:param id_person_requiring_assistance_type: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_person_requiring_assistance_type)
			data.is_active = False
			db.commit()

		return {
			'message': 'person requiring assistance type successfully removed'
		}