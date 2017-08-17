import cherrypy
from cause.api.management.core.route_url import RouteUrl
from cause.api.management.core.execute_api_class import ExecuteApiClass


class UrlForSurvey(ExecuteApiClass):
	def __init__(self):
		super(UrlForSurvey, self).__init__()

		RouteUrl('/survey/', 'Survey')
		RouteUrl('/survey/:id_survey', 'Survey')
		RouteUrl('/surveychoice/', 'SurveyChoice')
		RouteUrl('/surveychoice/:id_survey_question', 'SurveyChoice', 'GET', 'get')
		RouteUrl('/surveychoice/:id_survey_question/:is_active', 'SurveyChoice', 'GET', 'get')
		RouteUrl('/surveychoice/:id_survey_choice', 'SurveyChoice', 'DELETE', 'remove')
		RouteUrl('/surveyquestion/', 'SurveyQuestion')
		RouteUrl('/surveyquestion/:id_survey', 'SurveyQuestion', 'GET', 'get')
		RouteUrl('/surveyquestion/:id_survey/:is_active', 'SurveyQuestion', 'GET', 'get')
		RouteUrl('/surveyquestion/:id_survey_question', 'SurveyQuestion', 'DELETE', 'remove')

	@cherrypy.expose
	def survey(self, *args, **kwargs):
		return self.call_method('Survey', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveyquestion(self, *args, **kwargs):
		return self.call_method('SurveyQuestion', self.get_argument(args, kwargs))

	@cherrypy.expose
	def surveychoice(self, *args, **kwargs):
		return self.call_method('SurveyChoice', self.get_argument(args, kwargs))
