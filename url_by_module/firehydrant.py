from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForFireHydrant(ExecuteApiClass):
	def __init__(self):
		super(UrlForFireHydrant, self).__init__()

		RouteUrl('/firehydrant/', 'FireHydrant')
		RouteUrl('/firehydrant/:id_fire_hydrant', 'FireHydrant')
		RouteUrl('/firehydrantconnection/', 'FireHydrantConnection')
		RouteUrl('/firehydrantconnection/:id_fire_hydrant_connection', 'FireHydrant')
		RouteUrl('/firehydrantconnectiontype/', 'FireHydrantConnectionType')
		RouteUrl('/firehydrantconnectiontype/:id_fire_hydrant_connection_type', 'FireHydrantConnectionType')
		RouteUrl('/firehydranttype/', 'FireHydrantType')
		RouteUrl('/firehydranttype/:id_hydrant_type', 'FireHydrantType')
		RouteUrl('/operatortype/', 'OperatorType')
		RouteUrl('/operatortype/:id_operator_type', 'OperatorType')
		RouteUrl('/unitofmeasure/', 'UnitOfMeasure')
		RouteUrl('/unitofmeasure/:type', 'UnitOfMeasure')