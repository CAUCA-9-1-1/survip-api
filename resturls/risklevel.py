import uuid

from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.risk_level import RiskLevel as Table


class RiskLevel(Base):
	table_name = 'tbl_risk_level'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_risk_level=None, is_active=None):
		""" Return all information for risk level

		:param id_risk_level: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_risk_level is None and is_active is None:
				data = db.query(Table).all()
			elif id_risk_level is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_risk_level)

		return {
			'data': data
		}


	def create(self, body):
		""" Create a new risk level

		:param body: {
			name: JSON,
			sequence: INTEGER,
			code: INTEGER,
			color: STRING,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'code' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'code'")

		id_risk_level = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		sequence = body['sequence'] if 'sequence' in body else None
		color = body['color'] if 'color' in body else None

		with Database() as db:
			db.insert(Table(id_risk_level, id_language_content, sequence, body['code'], color))
			db.commit()

		return {
			'id_risk_level': id_risk_level,
			'message': 'risk level successfully created'
		}

	def modify(self, body):
		""" Modify a risk level

		:param body: {
			id_risk_level: UUID,
			name: JSON,
			sequence: INTEGER,
			code: INTEGER,
			color: STRING,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_risk_level' not in body:
			raise Exception("You need to pass a id_risk_level")

		with Database() as db:
			data = db.query(Table).get(body['id_risk_level'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'sequence' in body:
				data.sequence = body['sequence']
			if 'code' in body:
				data.code = body['code']
			if 'color' in body:
				data.color = body['color']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'risk level successfully modified'
		}

	def remove(self, id_risk_level):
		""" Remove a risk level

		:param id_risk_level: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_risk_level)
			data.is_active = False
			db.commit()

		return {
			'message': 'risk level successfully removed'
		}