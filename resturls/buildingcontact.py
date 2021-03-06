import uuid
from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base


class BuildingContact(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'assign',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building):
		""" Return all contact for one building

		:param id_building: UUID
		"""
		with Database() as db:
			data = db.get_all("SELECT * FROM tbl_building_contact WHERE id_building=%s;", (id_building,))

		return {
			'data': data
		}

	def assign(self, body):
		""" Assign new contact to building

		:param body: {
			id_building: UUID,
			first_name: STRING,
			last_name: STRING,
			phone_number: INTEGER,
			phone_extension: INTEGER,
			pager_number: INTEGER,
			pager_code: STRING,
			cellular_number: INTEGER,
			other_number: INTEGER
		}
		"""
		with Database() as db:
			db.execute("""INSERT INTO tbl_building_contact (
							id_building_contact, id_building, first_name, last_name, phone_number, phone_extension, pager_number, pager_code,
							cellular_number, other_number, created_on, is_active
						  ) VALUES(uuid_generate_v4(), %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), True);""", (
				body['id_building'], body['first_name'], body['last_name'], body['phone_number'], body['phone_extension'],
				body['pager_number'], body['pager_code'], body['cellular_number'], body['other_number']
			))

		return {
			'message': 'building contact successfully assigned'
		}

	def modify(self, body):
		""" Modify all information for building contact

		:param body: {
			id_building_contact: UUID,
			first_name: STRING,
			last_name: STRING,
			phone_number: INTEGER,
			phone_extension: INTEGER,
			pager_number: INTEGER,
			pager_code: STRING,
			cellular_number: INTEGER,
			other_number: INTEGER,
		}
		"""
		with Database() as db:
			db.execute("""UPDATE tbl_building_contact SET
							first_name=%s, last_name=%s, phone_number=%s, phone_extension=%s, pager_number=%s, pager_code=%s,
							cellular_number=%s, other_number=%s
						  WHERE id_building_contact=%s;""", (
				body['first_name'], body['last_name'], body['phone_number'], body['phone_extension'], body['pager_number'],
				body['pager_code'], body['cellular_number'], body['other_number'], body['id_building_contact']
			))

		return {
			'message': 'building contact successfully modified'
		}

	def remove(self, id_building_contact):
		""" Remove building contact

		:param id_building_contact: UUID
		"""
		with Database() as db:
			db.execute("UPDATE tbl_building_contact SET is_active=%s WHERE id_building_contact=%;", (
				False, id_building_contact
			))

		return {
			'message': 'building contact successfully removed'
		}