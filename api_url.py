import cherrypy
from cause.api.management.core.route_url import RouteUrl
from cause.api.management.api_url import ApiUrl as UrlForManagement
from .url_by_module.address import UrlForAddress
from .url_by_module.building import UrlForBuilding
from .url_by_module.firehydrant import UrlForFireHydrant
from .url_by_module.inspection import UrlForInspection
from .url_by_module.intervention_plan import UrlForInterventionPlan
from .url_by_module.survey import UrlForSurvey


class ApiUrl(UrlForSurvey, UrlForInterventionPlan, UrlForInspection,
             UrlForFireHydrant, UrlForAddress, UrlForBuilding, UrlForManagement):
	def __init__(self):
		super(ApiUrl, self).__init__()

		RouteUrl('/firesafetydepartment/', 'FireSafetyDepartment')
		RouteUrl('/webuserfiresafetydepartment/', 'WebuserFireSafetyDepartment')
		RouteUrl('/webuserfiresafetydepartment/:id_webuser', 'WebuserFireSafetyDepartment')
		RouteUrl('/picture/', 'Picture')

	@cherrypy.expose
	def firesafetydepartment(self, *args, **kwargs):
		return self.call_method('FireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def webuserfiresafetydepartment(self, *args, **kwargs):
		return self.call_method('WebuserFireSafetyDepartment', self.get_argument(args, kwargs))

	@cherrypy.expose
	def picture(self, *args, **kwargs):
		return self.call_method('Picture', self.get_argument(args, kwargs))
