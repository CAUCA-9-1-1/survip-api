from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.firestation import Firestation as Table


class Firestation(Base):
	table_name = "tbl_firestation"
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_firestation=None):
		""" Return all information for one firestation

		:param id_firestation: UUID
		"""
		with Database() as db:
			if id_firestation is None:
				data = db.query(Table).all()
			else:
				data = db.query(Table).filter(Table.id_firestation == id_firestation).all()

		return {
			'data': data
		}
