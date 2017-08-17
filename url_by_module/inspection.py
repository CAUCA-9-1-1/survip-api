from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForInspection(ExecuteApiClass):
	def __init__(self):
		super(UrlForInspection, self).__init__()

		RouteUrl('/inspection/', 'Inspection')
		RouteUrl('/inspection/:id_inspection', 'Inspection')
		RouteUrl('/inspectionanswer/', 'InspectionAnswer')
		RouteUrl('/inspectionanswer/:period_start/:period_end', 'InspectionAnswer', 'GET', 'get')
		RouteUrl('/inspectionbuilding/', 'InspectionBuilding')
		RouteUrl('/inspectionbyuser/', 'InspectionByUser')
		RouteUrl('/inspectionbyuser/:id_city', 'InspectionByUser')
		RouteUrl('/inspectionreport/:id_inspection_answer', 'InspectionReport', 'GET', 'pdf')
		RouteUrl('/inspectionstatistic/:period_start/:period_end', 'InspectionStatistic', 'GET', 'get')
