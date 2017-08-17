import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.lane import Lane as Table


class Lane(Base):
	table_name = 'tbl_lane'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_lane=None, is_active=None):
		""" Return all lane information

		:param id_lane: UUID
		:param is_active: Boolean
		"""
		with Database() as db:
			if id_lane is None and is_active is None:
				data = db.query(Table).all()
			elif id_lane is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_lane)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new lane

		:param body: {
			name: JSON,
			id_city: UUID
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_city' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_city'")

		id_lane = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		public_lane_code = body['public_lane_code'] if 'public_lane_code' in body else None
		generic_code = body['generic_code'] if 'generic_code' in body else None

		with Database() as db:
			db.insert(Table(id_lane, id_language_content, body['id_city'],
			                public_lane_code, generic_code))
			db.commit()

		return {
			'id_lane': id_lane,
			'message': 'lane successfully created'
		}

	def modify(self, body):
		""" Modify a lane

		:param body: {
			id_lane: UUID,
			name: JSON,
			id_city: UUID,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_lane' not in body:
			raise Exception("You need to pass a id_lane")

		with Database() as db:
			data = db.query(Table).filter(Table.id_lane == body['id_lane']).first()

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'id_city' in body:
				data.id_city = body['id_city']
			if 'public_lane_code' in body:
				data.public_lane_code = body['public_lane_code']
			if 'generic_code' in body:
				data.generic_code = body['generic_code']

			db.commit()

		return {
			'message': 'lane successfully modified'
		}

	def remove(self, id_lane):
		""" Remove a lane

		:param id_lane: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).filter(Table.id_lane == id_lane).first()
			data.is_active = False
			db.commit()

		return {
			'message': 'lane successfully removed'
		}