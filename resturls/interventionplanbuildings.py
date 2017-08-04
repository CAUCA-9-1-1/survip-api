import base64

from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from cause.api.survip.models.picture import Picture
from ..models.intervention_plan_building import InterventionPlanBuilding as PlanBuilding
from ..models.datatransfertobjects.BuildingForDisplay import BuildingForDisplay as Building


class InterventionPlanBuildings(Base):
	table_name = "tbl_intervention_plan_building"
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_intervention_plan):
		language = 'fr'

		buildings = []
		with Database() as db:
			result = db.query(PlanBuilding.id_intervention_plan_building, PlanBuilding.id_building,
							  PlanBuilding.id_picture, Building.id_language_content_name). \
				join((Building, PlanBuilding.id_building == Building.id_building)). \
				filter(PlanBuilding.is_active == '1',
					   PlanBuilding.id_intervention_plan == id_intervention_plan,
					   Building.is_active == '1'). \
				all()

			planbuildings = list(result)

			for planbuilding in planbuildings:
				alias = MultiLang.get_by_language(language, planbuilding[3])
				building = {
					'id_intervention_plan': planbuilding[0],
					'id_building': planbuilding[1],
					'picture': None,
					'alias': alias}
				if planbuilding[2] is not None:
					data = db.query(Picture).get(planbuilding[2])
					building['picture'] = base64.b64encode(data.picture).decode('utf-8')
				buildings.append(building)
		return {'data': buildings}
