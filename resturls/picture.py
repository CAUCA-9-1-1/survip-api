import base64
import uuid

import logging

from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.picture import Picture as Table


class Picture(Base):
	table_name = 'tbl_picture'
	mapping_method = {
		'GET': 'get',
		'PUT': 'put',
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
		if data:
			return {'id_picture': data.id_picture, 'picture': base64.b64encode(data.picture).decode('utf-8')}
		else:
			return {'message': 'No picture found'}

	def decode_picture_url(self, s):
		"""Add missing padding to string and return the decoded base64 string."""
		return base64.urlsafe_b64decode(s)
		"""log = logging.getLogger()
		s = str(s).strip()
		try:
			return base64.b64decode(s)
		except TypeError:
			padding = len(s) % 4
			if padding == 1:
				log.error("Invalid base64 string: {}".format(s))
				return ''
			elif padding == 2:
				s += b'=='
			elif padding == 3:
				s += b'='
			return base64.b64decode(s)"""

	def put(self, args):
		if 'picture' not in args:
			raise Exception("You need to pass a 'picture'")
		print('will encode to 64')
		picture = self.decode_picture_url(args['picture'])
		# picture = base64.b64decode()
		print('encoded')

		with Database() as db:
			if 'id_picture' in args and args["id_picture"]:
				print('existing picture')
				id_picture = args["id_picture"]
				pic_data = db.query(Table).get(id_picture)
				pic_data.picture = picture
			else:
				print('new picture')
				id_picture = uuid.uuid4()
				db.insert(Table(picture, id_picture))

			db.commit()

			print('saved')

		return {
			'id_picture': id_picture
		}


