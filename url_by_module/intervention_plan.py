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

	@cherrypy.expose
	def alarmpaneltype(self, *args, **kwargs):
		return self.call_method('AlarmPanelType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def constructiontype(self, *args, **kwargs):
		return self.call_method('ConstructionType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplangeneralinformations(self, *args, **kwargs):
		return self.call_method('InterventionPlanGeneralInformations', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplanbuildings(self, *args, **kwargs):
		return self.call_method('InterventionPlanBuildings', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplancourse(self, *args, **kwargs):
		return self.call_method('InterventionPlanCourse', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplancourseforlist(self, *args, **kwargs):
		return self.call_method('InterventionPlanCourseForList', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplancourselane(self, *args, **kwargs):
		return self.call_method('InterventionPlanCourseLane', self.get_argument(args, kwargs))

	@cherrypy.expose
	def interventionplancourselaneforlist(self, *args, **kwargs):
		return self.call_method('InterventionPlanCourseLaneForList', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firestation(self, *args, **kwargs):
		return self.call_method("Firestation", self.get_argument(args, kwargs))

	@cherrypy.expose
	def firestationforlist(self, *args, **kwargs):
		return self.call_method("FirestationForList", self.get_argument(args, kwargs))

	@cherrypy.expose
	def routedirection(self, *args, **kwargs):
		return self.call_method("RouteDirection", self.get_argument(args, kwargs))
