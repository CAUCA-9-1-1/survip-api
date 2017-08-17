import uuid

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from cause.api.survip.models.lane import Lane
from cause.api.survip.resturls.mappers.lane_light_mapper import LaneLightMapper
from ..models.intervention_plan_course import InterventionPlanCourse as Table
from ..models.intervention_plan_course_lane import InterventionPlanCourseLane as TableLane


class InterventionPlanCourse(Base):
	table_name = "tbl_intervention_plan_course"
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get_orientation_description(self, row):
		if row[2] == 1:
			return " (gauche)"
		elif row[2] == 2:
			return " (droite)"
		else:
			return ""

	def get_lanes(self, db, id_intervention_plan_course):
		data = db. \
			query(TableLane.id_intervention_plan_course_lane, TableLane.sequence, TableLane.direction, Lane). \
			join(Lane, Lane.id_lane == TableLane.id_lane). \
			filter(TableLane.is_active == '1', TableLane.id_intervention_plan_course == id_intervention_plan_course). \
			order_by(TableLane.sequence). \
			all()

		result = [{'id_intervention_plan_course_lane': r[0], 'sequence': r[1], 'description': LaneLightMapper.generate_full_name(r[3], 'fr') + self.get_orientation_description(r)} for r in data]

		return result

	def get(self, id_intervention_plan_course):
		with Database() as db:
			data = db.query(Table).filter(Table.is_active == '1', Table.id_intervention_plan_course == id_intervention_plan_course).first()
			lanes = self.get_lanes(db, id_intervention_plan_course)

		return {
			'data': {
				'course': data,
				'lanes': lanes
			}
		}

	def create(self, body):
		if 'id_firestation' not in body or 'id_intervention_plan' not in body:
			raise Exception("You need to pass a 'id_firestation' and 'id_intervention_plan'")

		id_intervention_plan_course = uuid.uuid4()

		with Database() as db:
			db.insert(Table(id_intervention_plan_course, body['id_intervention_plan'], body['id_firestation']))
			db.commit()

		return {
			'id_intervention_plan_course': id_intervention_plan_course,
			'message': "Intervention plan's course successfully created."
		}

	def modify(self, body):
		if 'id_intervention_plan_course' not in body:
			raise Exception("You need to pass a 'id_intervention_plan_course'")

		with Database() as db:
			data = db.query(Table).get(body['id_intervention_plan_course'])

			if 'id_firestation' in body:
				data.id_firestation = body['id_firestation']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {'message': "Intervention plan's course successfully modified."}

	def remove(self, id_intervention_plan_course):
		with Database() as db:
			data = db.query(Table).get(id_intervention_plan_course)
			data.is_active = False
			db.commit()

		return {'message': "Intervention plan's course successfully deleted."}
