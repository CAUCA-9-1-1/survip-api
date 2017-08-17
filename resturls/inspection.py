import uuid

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.inspection import Inspection as Table


class Inspection(Base):
	table_name = 'tbl_inspection'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_inspection=None, is_active=None):
		""" Return all inspection information

		:param id_inspection: UUID
		:param is_active: Boolean
		"""
		with Database() as db:
			if id_inspection is None and is_active is None:
				data = db.query(Table).all()
			elif id_inspection is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_inspection)

		return {
			'data': data
		}

	def create(self, body):
		""" Assign building inspection to someone

		:param body: {
			id_building: UUID,
			id_webuser: UUID,
			id_survey: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		if 'id_survey' not in body or 'id_building' not in body or 'id_webuser' not in body:
			raise Exception("You need to pass a 'id_webuser', 'id_building' and 'id_survey'")

		id_inspection = uuid.uuid4()
		with Database() as db:
			db.insert(Table(id_inspection, body['id_survey'], body['id_building'], body['id_webuser']))
			db.commit()

		return {
			'id_inspection': id_inspection,
			'message': 'inspection successfully created'
		}

	def modify(self, body):
		""" Mark inspection as done

		:param body: {
			id_inspection: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		if 'id_inspection' not in body:
			raise Exception("You need to pass a 'id_inspection'")

		with Database() as db:
			data = db.query(Table).filter(Table.id_inspection == body['id_inspection']).first()

			if 'id_webuser' in body:
				data.id_webuser = body['id_webuser']
			if 'is_active' in body:
				data.is_active = body['is_active']
			if 'is_completed' in body:
				data.is_completed = body['is_completed']
			db.commit()

		return {
			'message': 'inspection successfully modified'
		}

	def remove(self, id_inspection):
		""" Remove inspection

		:param id_inspection: UUID
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).filter(Table.id_inspection == id_inspection).first()
			data.is_active = False
			db.commit()

		return {
			'message': 'inspection successfully removed'
		}