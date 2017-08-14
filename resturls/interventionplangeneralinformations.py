from sqlalchemy.orm import joinedload

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from cause.api.survip.models.lane import Lane
from cause.api.survip.resturls.mappers.lane_light_mapper import LaneLightMapper
from ..models.datatransfertobjects.BuildingForDisplay import BuildingForDisplay as Building
from ..models.intervention_plan import InterventionPlan as Plan, InterventionPlan
from ..models.intervention_plan_building import InterventionPlanBuilding as PlanBuilding
from ..resturls.mappers.building_for_display_loader import BuildingForDisplayLoader


class InterventionPlanGeneralInformations(Base):
	table_name = 'tbl_intervention_plan'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, language, id_intervention_plan):
		""" Return all information for intervention plan

		:param id_intervention_plan: UUID
		"""
		with Database() as db:
			plan = db.query(Plan).\
				filter(Plan.is_active == '1', Plan.id_intervention_plan == id_intervention_plan).\
				first()
			data = {}
			if plan is not None:
				data['id'] = plan.id_intervention_plan
				data['plan_number'] = plan.number
				data['plan_name'] = plan.plan_name
				data['id_lane_transversal'] = plan.id_lane_transversal
				data['id_picture_site_plan'] = plan.id_picture_site_plan
				data['active'] = True
				planbuilding = db.query(PlanBuilding).\
					filter(PlanBuilding.is_active == '1',
						   PlanBuilding.id_intervention_plan == id_intervention_plan,
						   PlanBuilding.is_parent == '1').\
					first()

				if planbuilding is not None:
					data['other_information'] = planbuilding.additional_information
					data['created_on'] = planbuilding.created_on

					building = db.query(Building). \
						filter(Building.is_active == '1', Building.id_building == planbuilding.id_building). \
						first()
					if building is not None:
						BuildingForDisplayLoader.set_address_description(language, building)
						data['main_building_address'] = building.full_address
						data['id_city'] = building.id_city
						data['main_building_id_lane'] = building.id_lane
						data['main_building_alias'] = building.alias_name
						data['main_building_id_risk_level'] = building.id_risk_level
						data['main_building_risk_level_name'] = building.risk_level_name
						data['main_building_matricule'] = building.matricule
						data['main_building_affectation'] = building.utilisation_code_name
						lane = db.query(Lane). \
							filter_by(id_lane=building.id_lane). \
							options(joinedload(Lane.lane_public_code), joinedload(Lane.lane_generic_code)). \
							first()
						data['main_building_lane_name'] = LaneLightMapper.generate_full_name(lane, language)

		return {'data': data}

	def camelify(self, out):
		return (''.join(["_" + x.lower() if i < len(out) - 1 and x.isupper() and out[i + 1].islower()
						 else x.lower() + "_" if i < len(out) - 1 and x.islower() and out[i + 1].isupper()
		else x.lower() for i, x in enumerate(list(out))])).lstrip('_').replace('__', '_')

	def modify(self, id_plan, field_name, value):
		field_name = self.camelify(field_name)
		with Database() as db:
			db.query(Plan).filter_by(id_intervention_plan=id_plan).update({field_name: value})
			db.commit()
			return {'message': '{0} correctly pushed to {1}'.format(value, field_name)}
