from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from cause.api.survip.models.firestation import Firestation
from ..models.intervention_plan_course import InterventionPlanCourse as Table


class InterventionPlanCourseForList(Base):
	table_name = "tbl_intervention_plan_course"
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		with Database() as db:
			data = db.\
				query(Table.id_intervention_plan_course, Firestation.station_name).\
				join(Firestation, Firestation.id_firestation == Table.id_firestation).\
				filter(Table.is_active == '1', Table.id_intervention_plan == id_intervention_plan).\
				all()

			result = [{'id_intervention_plan_course': r[0], 'description': r[1]} for r in data]

		return {'data': result}
