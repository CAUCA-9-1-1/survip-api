import uuid

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.intervention_plan_course import InterventionPlanCourse as Table


class InterventionPlanCourse(Base):
	table_name = "tbl_intervention_plan_course"
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_intervention_plan_course):
		with Database() as db:
			data = db.query(Table).filter(Table.is_active == '1', Table.id_intervention_plan_course == id_intervention_plan_course).all()

		return {'data': data}

	def create(self, args):
		if 'id_firestation' not in args or 'id_intervention_plan' not in args:
			raise Exception("You need to pass a 'id_firestation' and 'id_intervention_plan'")

		id_intervention_plan_course = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_intervention_plan_course, args['id_intervention_plan_course'], args['id_firestation']))
			db.commit()

		return {
			'id_intervention_plan_course': id_intervention_plan_course,
			'message': "Intervention plan's course successfully created."
		}

	def modify(self, args):
		if 'id_intervention_plan_course' not in args:
			raise Exception("You need to pass a 'id_intervention_plan_course'")

		with Database() as db:
			data = db.query(Table).get(args['id_intervention_plan_course'])

			if 'id_firestation' in args:
				data.direction = args['id_firestation']
			if 'is_active' in args:
				data.is_active = args['is_active']

			db.commit()

		return {'message': "Intervention plan's course successfully modified."}

	def delete(self, id_intervention_plan_course):
		with Database() as db:
			data = db.query(Table).get(id_intervention_plan_course)
			data.is_active = False
			db.commit()

		return {'message': "Intervention plan's course successfully deleted."}
