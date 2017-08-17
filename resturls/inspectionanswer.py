import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.session import Session
from cause.api.management.resturls.base import Base
from cause.api.management.resturls.webuser import Webuser
from .inspection import Inspection
from .building import Building


class InspectionAnswer(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'answer',
		'POST': 'answer_question',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, period_start, period_end):
		""" Return all information for inspection

		:param period_start: TIMESTAMP
		:param period_end: TIMESTAMP
		"""
		with Database() as db:
			data = db.get_all("""SELECT * FROM tbl_inspection_answer
								  LEFT JOIN tbl_inspection ON tbl_inspection.id_inspection = tbl_inspection_answer.id_inspection
		                          WHERE answered_on>=%s AND answered_on<%s;""", (period_start, period_end))

		for key, row in enumerate(data):
			data[key]['building'] = Building().get(row['id_building'])
			data[key]['webuser'] = Webuser().get(row['id_webuser'])

		return {
			'data': data
		}

	def answer(self, body):
		""" Add an answer to a survey

		:param body: {
			id_inspection: UUID,
			has_refuse: BOOLEAN,
			reason_for_refusal: String,
			is_absent: BOOLEAN,
			is_seasonal: BOOLEAN,
			is_vacant: BOOLEAN
		}
		"""
		is_completed=False
		id_inspection_answer = uuid.uuid4()

		with Database() as db:
			db.execute("""INSERT INTO
						tbl_inspection_answer(id_inspection_answer, id_inspection, id_webuser, answered_on, has_refuse, reason_for_refusal, is_absent, is_seasonal, is_vacant)
						VALUES(%s, %s, %s, NOW(), %s, %s, %s, %s, %s);""", (
				id_inspection_answer, body['id_inspection'], Session.get('userId'), body['has_refuse'], body['reason_for_refusal'], body['is_absent'], body['is_seasonal'], body['is_vacant']
			))

		if body['has_refuse'] is False and body['is_absent'] is False:
			is_completed = True
			Inspection().complete({
				'id_inspection': body['id_inspection']
			})

		return {
			'is_completed': is_completed,
			'id_inspection_answer': id_inspection_answer,
			'message': 'survey successfully answered'
		}

	def answer_question(self, body):
		""" Add an answer to a question of survey

		:param body: {
			id_inspection_answer: UUID,
			id_survey_question: UUID,
			id_survey_choice: UUID,
			answer: String
		}
		"""
		id_inspection_question = uuid.uuid4()

		with Database() as db:
			db.execute("""INSERT INTO
						tbl_inspection_question(id_inspection_question, id_inspection_answer, id_survey_question, id_survey_choice, answer)
						VALUES(%s, %s, %s, %s, %s);""", (
				id_inspection_question, body['id_inspection_answer'], body['id_survey_question'], body['id_survey_choice'], body['answer']
			))

		return {
			'message': 'survey successfully answered to question'
		}