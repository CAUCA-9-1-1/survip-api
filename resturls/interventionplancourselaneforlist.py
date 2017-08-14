from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from cause.api.survip.models.lane import Lane
from cause.api.survip.resturls.mappers.lane_light_mapper import LaneLightMapper
from ..models.intervention_plan_course_lane import InterventionPlanCourseLane as Table


class InterventionPlanCourseLaneForList(Base):
	table_name = "tbl_intervention_plan_course_lane"
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get_orientation_description(self, row):
		if row[1] == 1:
			return " (gauche)"
		elif row[1] == 2:
			return " (droite)"
		else:
			return ""

	def get(self, id_intervention_plan_course):
		with Database() as db:
			data = db. \
				query(Table.id_intervention_plan_course_lane, Table.direction, Lane). \
				join(Lane, Lane.id_lane == Table.id_lane). \
				filter(Table.is_active == '1', Table.id_intervention_plan_course == id_intervention_plan_course). \
				all()

			result = [{'id_intervention_plan_course_lane': r[0], 'description': LaneLightMapper.generate_full_name(r[2], 'fr') + self.get_orientation_description(r)} for r in data]

		return {'data': result}
