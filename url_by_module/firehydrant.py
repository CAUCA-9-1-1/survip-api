import cherrypy
from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForFireHydrant(ExecuteApiClass):
	def __init__(self):
		super(UrlForFireHydrant, self).__init__()

		RouteUrl('/firehydrant/', 'FireHydrant')
		RouteUrl('/firehydrant/:id_fire_hydrant', 'FireHydrant')
		RouteUrl('/firehydrantconnection/', 'FireHydrantConnection')
		RouteUrl('/firehydrantconnection/:id_fire_hydrant_connection', 'FireHydrant')
		RouteUrl('/firehydranttype/', 'FireHydrantType')
		RouteUrl('/firehydranttype/:id_hydrant_type', 'FireHydrantType')
		RouteUrl('/firehydrantconnectiontype/', 'FireHydrantConnectionType')
		RouteUrl('/firehydrantconnectiontype/:id_fire_hydrant_connection_type', 'FireHydrantConnectionType')
		RouteUrl('/operatortype/', 'OperatorType')
		RouteUrl('/operatortype/:id_operator_type', 'OperatorType')
		RouteUrl('/unitofmeasure/', 'UnitOfMeasure')
		RouteUrl('/unitofmeasure/:type', 'UnitOfMeasure')

	@cherrypy.expose
	def firehydrant(self, *args, **kwargs):
		return self.call_method('FireHydrant', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firehydrantconnection(self, *args, **kwargs):
		return self.call_method('FireHydrantConnection', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firehydranttype(self, *args, **kwargs):
		return self.call_method('FireHydrantType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def firehydrantconnectiontype(self, *args, **kwargs):
		return self.call_method('FireHydrantConnectionType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def operatortype(self, *args, **kwargs):
		return self.call_method('OperatorType', self.get_argument(args, kwargs))

	@cherrypy.expose
	def unitofmeasure(self, *args, **kwargs):
		return self.call_method('UnitOfMeasure', self.get_argument(args, kwargs))
