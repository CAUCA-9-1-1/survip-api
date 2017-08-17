import uuid
from sqlalchemy import asc
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.survey import SurveyQuestion as Table


class SurveyQuestion(Base):
	table_name = 'tbl_survey_question'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_survey=None, is_active=None):
		""" Return all question for one survey

		:param id_survey: UUID
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			if is_active is None:
				data = db.query(Table).filter(
					Table.id_survey == id_survey
				).order_by(asc(Table.sequence)).all()
			else:
				data = db.query(Table).filter(
					Table.id_survey == id_survey,
					Table.is_active == is_active,
				).order_by(asc(Table.sequence)).all()

		return {
			'data': data
		}

	def create(self, body):
		""" Create a question for a survey

		:param body: {
			id_survey: UUID,
			title: JSON,
			description: JSON,
			sequence: INTEGER,
			id_survey_question_next: UUID
		}
		"""
		if self.has_permission('RightTPI') is False:
			self.no_access()

		if 'title' not in body or 'description' not in body or 'id_survey' not in body:
			raise Exception("You need to pass a 'title', 'description' and 'id_survey'")

		id_survey_question = uuid.uuid4()
		id_language_content_title = MultiLang.set(body['title'], True)
		id_language_content_description = MultiLang.set(body['description'], True)
		next_question = body['id_survey_question_next'] if 'id_survey_question_next' in body and body['id_survey_question_next'] != '' else None
		sequence = int(body['sequence']) if 'sequence' in body else 0
		question_type = body['question_type'] if 'question_type' in body else 'text'

		with Database() as db:
			db.insert(Table(
				id_survey_question, body['id_survey'], id_language_content_title,
				id_language_content_description, next_question, sequence, question_type))
			db.commit()

		return {
			'id_survey_question': id_survey_question,
			'message': 'survey question successfully created'
		}

	def modify(self, body):
		if self.has_permission('RightTPI') is False:
			self.no_access()

		if 'id_survey_question' not in body:
			raise Exception("You need to pass a id_survey_question")
		if 'step' in body:
			return self.change_sequence(body)

		next_question = body['id_survey_question_next'] if 'id_survey_question_next' in body and body['id_survey_question_next'] != '' else None

		with Database() as db:
			data = db.query(Table).get(body['id_survey_question'])
			data.id_survey_question_next = next_question

			if 'title' in body:
				data.id_language_content_title = MultiLang.set(body['title'])
			if 'description' in body:
				data.id_language_content_description = MultiLang.set(body['description'])
			if 'sequence' in body:
				data.sequence = body['sequence']
			if 'question_type' in body:
				data.question_type = body['question_type']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'survey question successfully modified'
		}

	def remove(self, id_survey_question):
		if self.has_permission('RightTPI') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_survey_question)
			data.is_active = False
			db.commit()

		return {
			'message': 'survey question successfully removed'
		}

	def change_sequence(self, args):
		with Database() as db:
			question = db.query(Table).get(args['id_survey_question'])
			question.sequence = (int(question.sequence) + int(args['step']))
			db.execute("""UPDATE tbl_survey_question
							SET sequence=(sequence + %s)
							WHERE sequence=%s AND id_survey=%s;""", (
				(int(args['step']) * -1), question.sequence, question.id_survey))
			db.commit()

		return {
			'message': 'survey question successfully change sequence'
		}
