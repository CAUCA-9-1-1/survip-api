import uuid

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.intervention_plan_course_lane import InterventionPlanCourseLane as Table


class InterventionPlanCourseLane(Base):
	table_name = "tbl_intervention_plan_course_lane"
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_intervention_plan_course_lane):
		with Database() as db:
			data = db.query(Table).filter(Table.is_active == '1', Table.id_intervention_plan_course_lane == id_intervention_plan_course_lane).first()

		return {'data': data}

	def create(self, body):
		if 'id_lane' not in body or 'direction' not in body or 'id_intervention_plan_course' not in body or 'sequence' not in body:
			raise Exception("You need to pass a 'direction', 'id_lane', 'sequence' and 'id_intervention_plan_course'")

		id_intervention_plan_course_lane = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_intervention_plan_course_lane, body['id_intervention_plan_course'],
							body['id_lane'], body['direction'], body['sequence']))
			db.commit()

		return {
			'id_intervention_plan_course_lane': id_intervention_plan_course_lane,
			'message': "Course's lane successfully created."
		}

	def modify(self, body):
		if 'id_intervention_plan_course_lane' not in body:
			raise Exception("You need to pass a 'id_intervention_plan_course_lane'")

		with Database() as db:
			data = db.query(Table).get(body['id_intervention_plan_course_lane'])

			if 'direction' in body:
				data.direction = body['direction']
			if 'id_lane' in body:
				data.id_lane = body['id_lane']
			if 'is_active' in body:
				data.is_active = body['is_active']
			if 'sequence' in body:
				data.sequence = body['sequence']

			db.commit()

		return {'message': 'Course lane successfully modified.'}

	def remove(self, id_intervention_plan_course_lane):
		print('deleteeeeeeee')
		with Database() as db:
			lane = db.query(Table).get(id_intervention_plan_course_lane)

			lanes = db.query(Table).\
				filter(Table.is_active == '1', Table.id_intervention_plan_course == lane.id_intervention_plan_course). \
				order_by(Table.sequence). \
				all()

			sequence = 1

			for item in lanes:
				if item.id_intervention_plan_course_lane == lane.id_intervention_plan_course_lane:
					# print('deactivate')
					item.is_active = '0'
				else:
					item.sequence = sequence
					sequence = sequence + 1

			db.commit()

		return {'message': "Intervention plan course's lane successfully deleted."}
