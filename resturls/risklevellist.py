from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.risk_level import RiskLevel as Table
from cause.api.management.resturls.webuser import Webuser


class RiskLevelList(Base):
	table_name = 'tbl_risk_level'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_risk_level=None):
		""" Return all information for risk level

		:param id_risk_level: STRING
		"""
		language = Webuser().get_attribute('language')

		with Database() as db:
			if id_risk_level is None:
				data = db.query(Table).filter(Table.is_active == '1').all()
				if data is not None:
					for risk in data:
						risk.fullName = self.get_name(risk, language)
			else:
				data = db.query(Table).filter(Table.is_active == '1').first()
				if data is not None:
					data.fullName = self.get_name(data, language)

		return {'data': data}
	
	def get_name(self, risk, language):
		if language in risk.name:
			return risk.name[language]
		else:
			return risk.name['fr']

