from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from cause.api.survip.models.picture import Picture
from ..models.intervention_plan_building import InterventionPlanBuilding as PlanBuilding
from ..models.datatransfertobjects.BuildingForDisplay import BuildingForDisplay as Building
import base64


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
		data = {'id_building': None, 'id_intervention_plan_building': None, 'id_picture': None, 'picture': None, 'alias': None}

		with Database() as db:
			planbuilding = db.query(PlanBuilding.id_intervention_plan_building, PlanBuilding.id_building,
									PlanBuilding.id_picture). \
				filter(PlanBuilding.is_active == '1',
					   PlanBuilding.id_intervention_plan == id_intervention_plan,
					   PlanBuilding.is_parent == '1'). \
				first()

			if planbuilding is not None:
				data['id_picture'] = planbuilding.id_picture
				data['id_building'] = planbuilding.id_building
				data['id_intervention_plan_building'] = planbuilding.id_intervention_plan_building
				picture = db.query(Picture.picture).filter(Picture.id_picture == planbuilding.id_picture).first()
				if picture is not None:
					print("Picture is of type {0}".format(type(picture.picture)))

					data['picture'] = base64.b64encode(picture.picture)
				building = db.query(Building.id_language_content_name). \
					filter(Building.is_active == '1', Building.id_building == planbuilding.id_building). \
					first()

				print(data['picture']);

				if building is not None:
					data['alias'] = MultiLang.get_by_language(language, building.id_language_content_name)


		return {'data': data}
