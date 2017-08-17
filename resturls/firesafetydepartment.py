import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.fire_safety_department import FireSafetyDepartment as Table


class FireSafetyDepartment(Base):
	table_name = 'tbl_fire_safety_department'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_fire_safety_department=None, is_active=None):
		""" Return all information for one fire safety department

		:param id_fire_safety_department: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_fire_safety_department is None and is_active is None:
				data = db.query(Table).all()
			elif id_fire_safety_department is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_fire_safety_department)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new fire safety department

		:param body: {
			name: JSON,
			id_county: UUID,
			language: STRING,
			is_active: BOOLEAN
		}
		"""
		id_fire_safety_department = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		id_county = body['id_county'] if 'id_county' in body else None
		language = body['language'] if 'language' in body else None

		with Database() as db:
			db.insert(Table(id_fire_safety_department, id_language_content, id_county, language))
			db.commit()

		return {
			'id_fire_safety_department': id_fire_safety_department,
			'message': 'fire safety department successfully created'
		}

	def modify(self, body):
		""" Modify a fire safety department

		:param body: {
			id_fire_safety_department: UUID,
			name: JSON,
			is_active: BOOLEAN
		}
		"""
		if 'id_fire_safety_department' not in body:
			raise Exception("You need to pass a id_fire_safety_department")

		with Database() as db:
			data = db.query(Table).get(body['id_fire_safety_department'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'id_county' in body:
				data.id_county = body['id_county']
			if 'language' in body:
				data.language = body['language']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'fire safety department successfully modified'
		}

	def remove(self, id_fire_safety_department):
		""" Remove a fire safety department

		:param id_fire_safety_department: UUID
		"""
		with Database() as db:
			data = db.query(Table).get(id_fire_safety_department)
			data.is_active = False
			db.commit()

		return {
			'message': 'fire safety department successfully removed'
		}
