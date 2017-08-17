import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.survey import SurveyChoice as Table


class SurveyChoice(Base):
	table_name = 'tbl_survey_choice'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey_question=None, is_active=None):
		""" Return all choices for one question

		:param id_survey_question: UUID
		:param is_active: BOOLEAN
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			if is_active is None:
				data = db.query(Table).filter(Table.id_survey_question == id_survey_question).all()
			else:
				data = db.query(Table).filter(
					Table.id_survey_question == id_survey_question,
					Table.is_active == is_active,
				).all()

		return {
			'data': data
		}

	def create(self, body):
		""" Create a choice for a question on survey

		:param body: {
			id_survey_question: UUID,
			sequence: INTEGER,
			description: JSON,
			id_survey_question_next: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()
		if 'id_survey_question' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'id_survey_question'")

		id_survey_choice = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		sequence = int(body['sequence']) if 'sequence' in body else 0
		next_question = body['id_survey_question_next'] if 'id_survey_question_next' in body and body['id_survey_question_next'] != '' else None

		with Database() as db:
			db.insert(Table(id_survey_choice, body['id_survey_question'], id_language_content, next_question, sequence))
			db.commit()

		return {
			'id_survey_choice': id_survey_choice,
			'message': 'survey choice successfully created'
		}

	def modify(self, body):
		if self.has_permission('RightTPI') is False:
			self.no_access()

		next_question = body['id_survey_question_next'] if 'id_survey_question_next' in body else None

		with Database() as db:
			data = db.query(Table).get(body['id_survey_choice'])
			data.id_survey_question_next = next_question

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'sequence' in body:
				data.sequence = MultiLang.set(body['sequence'])
			if 'is_active' in body:
				data.is_active = MultiLang.set(body['is_active'])

			db.commit()

		return {
			'message': 'survey choice successfully modified'
		}

	def remove(self, id_survey_choice):
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_survey_choice)
			data.is_active = False
			db.commit()

		return {
			'message': 'survey choice successfully removed'
		}