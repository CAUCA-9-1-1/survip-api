from cause.api.management.resturls.base import Base


class RouteDirection(Base):
	table_name = ""
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self):
		""" Return all route direction

		:param id_firestation: UUID
		"""
		data = [{'id': 0, 'description': 'tout droit'}, {'id': 1, 'description': 'gauche'}, {'id': 2, 'description': 'droite'}]

		return {
			'data': data
		}
