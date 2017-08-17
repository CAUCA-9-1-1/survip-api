from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForAddress(ExecuteApiClass):
	def __init__(self):
		super(UrlForAddress, self).__init__()

		RouteUrl('/city/', 'City')
		RouteUrl('/city/:id_city', 'City')
		RouteUrl('/citylanes/:language/:id_city_filter', 'CityLanes', 'GET', 'get')

		RouteUrl('/citytype/', 'CityType')
		RouteUrl('/citytype/:id_city_type', 'CityType')

		RouteUrl('/country/', 'Country')
		RouteUrl('/country/:id_country', 'Country')

		RouteUrl('/county/', 'County')
		RouteUrl('/county/:id_county', 'County')

		RouteUrl('/lane/', 'Lane')
		RouteUrl('/lane/:id_lane', 'Lane')
		RouteUrl('/lanelight/:language/:id_lane', 'LaneLight')

		RouteUrl('/region/', 'Region')
		RouteUrl('/region/:id_region', 'Region')

		RouteUrl('/state/', 'State')
		RouteUrl('/state/:id_state', 'State')
