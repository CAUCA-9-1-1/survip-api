from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.picture import Picture as Table


class Picture(Base):
	table_name = 'tbl_picture'
	mapping_method = {
		'GET': 'get',
		'PUT': '',
		'POST': '',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_picture):
		""" Return all information for picture

		:param id_picture: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
				data = db.query(Table).get(id_picture)
		print(data.picture)
		return data.picture
