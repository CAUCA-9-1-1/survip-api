from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForInterventionPlan(ExecuteApiClass):
	def __init__(self):
		super(UrlForInterventionPlan, self).__init__()

		RouteUrl('/alarmpaneltype/', 'AlarmPanelType')
		RouteUrl('/alarmpaneltype/:id_alarm_panel_type', 'AlarmPanelType')

		RouteUrl('/constructiontype/', 'ConstructionType')
		RouteUrl('/constructiontype/:id_construction_type', 'ConstructionType')

		RouteUrl('/interventionplangeneralinformations/', 'InterventionPlanGeneralInformations')
		RouteUrl('/interventionplangeneralinformations/:language/:id_intervention_plan', 'InterventionPlanGeneralInformations', 'GET', 'get')

		RouteUrl('/interventionplanbuildings/:id_intervention_plan', 'InterventionPlanBuildings', 'GET', 'get')

		RouteUrl('/interventionplancourse/', 'InterventionPlanCourse')
		RouteUrl('/interventionplancourse/:id_intervention_plan_course', 'InterventionPlanCourse')
		RouteUrl('/interventionplancourseforlist/:id_intervention_plan', 'InterventionPlanCourseForList', 'GET', 'get')

		RouteUrl('/interventionplancourselane/', 'InterventionPlanCourseLane')
		RouteUrl('/interventionplancourselane/:id_intervention_plan_course_lane', 'InterventionPlanCourseLane')
		RouteUrl('/interventionplancourselaneforlist/:id_intervention_plan_course', 'InterventionPlanCourseLaneForList', 'GET', 'get')

		RouteUrl('/firestation/', 'Firestation')
		RouteUrl('/firestationforlist/:id_firestation', 'FirestationForList', 'GET', 'get')

		RouteUrl('/routedirection/', 'RouteDirection', 'GET', 'get')
