from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.firestation import Firesteation as Table


class FirestationForList(Base):
	table_name = "tbl_firestation"
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_firestation=None):
		""" Return basic informations for one firestation

		:param id_firestation: UUID
		"""
		with Database() as db:
			if id_firestation is None:
				data = db.query(Table.id_firestation, Table.station_name).all()
			else:
				data = db.query(Table.id_firestation, Table.station_name).filter(Table.id_firestation == id_firestation).all()

			result = [{'id_firestation': r[0], 'station_name': r[1]} for r in data]

		return {
			'data': result
		}
