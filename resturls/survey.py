import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.inspection import Inspection
from ..models.survey import Survey as Table


class Survey(Base):
	table_name = 'tbl_survey'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey=None):
		""" Return the survey information

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			if id_survey is None:
				data = db.query(Table).all()
			else:
				data = db.query(Table).get(id_survey)

		return {
			'data': data
		}

	def create(self, body):
		""" Create a new survey

		:param body: {
			name: JSON,
			survey_type: ENUM('test'),
			questions: JSON
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		id_survey = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)

		with Database() as db:
			db.insert(Table(id_survey, id_language_content, body['survey_type']))
			db.commit()

		return {
			'id_survey': id_survey,
			'message': 'survey successfully created'
		}

	def modify(self, body):
		""" Modify a survey

		:param body: {
			id_survey: UUID,
			name: JSON,
			survey_type: ENUM('test'),
			is_active: BOOLEAN,
			questions: JSON
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		if 'id_survey' not in body:
			raise Exception("You need to pass a id_survey")

		with Database() as db:
			inspection = db.query(Inspection).filter(
				Inspection.id_survey == body['id_survey'],
				Inspection.is_completed == True,
			).all()

			if len(inspection) > 0:
				self.remove(body['id_survey'])
				self.create(body)
			else:
				data = db.query(Table).get(body['id_survey'])

				if 'name' in body:
					data.id_language_content_name = MultiLang.set(body['name'])

				if 'survey_type' in body:
					data.survey_type = body['survey_type']
				if 'is_active' in body:
					data.is_active = body['is_active']

				db.commit()

		return {
			'message': 'survey successfully modified'
		}

	def remove(self, id_survey):
		""" Remove a survey

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_survey)
			data.is_active = False
			db.commit()

		return {
			'message': 'survey successfully removed'
		}
