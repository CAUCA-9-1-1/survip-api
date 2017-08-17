from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForBuilding(ExecuteApiClass):
	def __init__(self):
		super(UrlForBuilding, self).__init__()

		RouteUrl('/building/', 'Building')
		RouteUrl('/building/:id_building', 'Building')

		RouteUrl('/buildingcontact/', 'BuildingContact')
		RouteUrl('/buildingcontact/:id_building', 'BuildingContact', 'GET', 'get')
		RouteUrl('/buildingcontact/:id_building_contact', 'BuildingContact', 'DELETE', 'remove')

		RouteUrl('/buildinghazardousmaterial/', 'BuildingHazardousMaterial')
		RouteUrl('/buildinghazardousmaterial/:id_building', 'BuildingHazardousMaterial', 'GET', 'get')

		RouteUrl('/buildingpersonrequiringassistance/', 'BuildingPersonRequiringAssistance')
		RouteUrl('/buildingpersonrequiringassistance/:id_building', 'BuildingPersonRequiringAssistance', 'GET', 'get')
		RouteUrl('/buildingpersonrequiringassistance/:id_building_person_requiring_assistance', 'BuildingPersonRequiringAssistance', 'DELETE', 'remove')

		RouteUrl('/hazardousmaterial/', 'HazardousMaterial')
		RouteUrl('/hazardousmaterial/:id_hazardous_material', 'HazardousMaterial')

		RouteUrl('/personrequiringassistancetype/', 'PersonRequiringAssistanceType')
		RouteUrl('/personrequiringassistancetype/:id_person_requiring_assistance_type', 'PersonRequiringAssistanceType')

		RouteUrl('/risklevel/', 'RiskLevel')
		RouteUrl('/risklevel/:id_risk_level', 'RiskLevel')
		RouteUrl('/risklevellist/:language', 'RiskLevelList', 'GET', 'get')

		RouteUrl('/utilisationcode/', 'UtilisationCode')
		RouteUrl('/utilisationcode/:id_utilisation_code', 'UtilisationCode')
