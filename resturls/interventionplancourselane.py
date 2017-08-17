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

	def create(self, args):
		if 'id_lane' not in args or 'direction' not in args or 'id_intervention_plan_course' not in args or 'sequence' not in args:
			raise Exception("You need to pass a 'direction', 'id_lane', 'sequence' and 'id_intervention_plan_course'")

		id_intervention_plan_course_lane = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_intervention_plan_course_lane, args['id_intervention_plan_course'],
							args['id_lane'], args['direction'], args['sequence']))
			db.commit()

		return {
			'id_intervention_plan_course_lane': id_intervention_plan_course_lane,
			'message': "Course's lane successfully created."
		}

	def modify(self, args):
		if 'id_intervention_plan_course_lane' not in args:
			raise Exception("You need to pass a 'id_intervention_plan_course_lane'")

		with Database() as db:
			data = db.query(Table).get(args['id_intervention_plan_course_lane'])

			if 'direction' in args:
				data.direction = args['direction']
			if 'id_lane' in args:
				data.id_lane = args['id_lane']
			if 'is_active' in args:
				data.is_active = args['is_active']
			if 'sequence' in args:
				data.sequence = args['sequence']

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
