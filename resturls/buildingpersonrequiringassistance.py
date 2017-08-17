import uuid
from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base
from ..models.building_person_requiring_assistance import BuildingPersonRequiringAssistance as Table


class BuildingPersonRequiringAssistance(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_building):
		""" Return all PRSA for one building

		:param id_building: UUID
		"""
		with Database() as db:
			data = db.query(Table).filter(Table.id_building == id_building).all()

		return {
			'data': data
		}

	def create(self, body):
		""" Assign new PRSA to building

		:param args: {
			id_building: UUID,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_building' not in body or 'id_person_requiring_assistance_type' not in body or 'pra_name' not in body:
			raise Exception("You need to pass a 'id_building', 'id_person_requiring_assistance_type' and 'pra_name'")

		id_building_person_requiring_assistance = uuid.uuid4()
		day_resident_count = body['day_resident_count'] if 'day_resident_count' in body else 0
		evening_resident_count = body['evening_resident_count'] if 'evening_resident_count' in body else 0
		night_resident_count = body['night_resident_count'] if 'night_resident_count' in body else 0
		day_is_approximate = body['day_is_approximate'] if 'day_is_approximate' in body else False
		evening_is_approximate = body['evening_is_approximate'] if 'evening_is_approximate' in body else False
		night_is_approximate = body['night_is_approximate'] if 'night_is_approximate' in body else False
		description = body['description'] if 'description' in body else None
		floor = body['floor'] if 'floor' in body else None
		local = body['local'] if 'local' in body else None
		contact_name = body['contact_name'] if 'contact_name' in body else None
		contact_phone_number = body['contact_phone_number'] if 'contact_phone_number' in body else None

		with Database() as db:
			db.insert(Table(
				id_building_person_requiring_assistance, body['id_building'], body['id_person_requiring_assistance_type'], day_resident_count,
				evening_resident_count, night_resident_count, day_is_approximate, evening_is_approximate, night_is_approximate, description,
				body['pra_name'], floor, local, contact_name, contact_phone_number))
			db.commit()

		return {
			'id_building_person_requiring_assistance': id_building_person_requiring_assistance,
			'message': 'building person requiring assistance successfully assigned'
		}

	def modify(self, body):
		""" Modify all information for building person requiring assistance

		:param body: {
			id_building_person_requiring_assistance: UUID,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_building_person_requiring_assistance' not in body:
			raise Exception("You need to pass a id_building_person_requiring_assistance")

		with Database() as db:
			data = db.query(Table).get(body['id_building_person_requiring_assistance'])

			if 'id_building' in body:
				data.id_building = body['id_building']
			if 'id_person_requiring_assistance_type' in body:
				data.id_person_requiring_assistance_type = body['id_person_requiring_assistance_type']
			if 'day_resident_count' in body:
				data.day_resident_count = body['day_resident_count']
			if 'evening_resident_count' in body:
				data.evening_resident_count = body['evening_resident_count']
			if 'night_resident_count' in body:
				data.night_resident_count = body['night_resident_count']
			if 'day_is_approximate' in body:
				data.day_is_approximate = body['day_is_approximate']
			if 'evening_is_approximate' in body:
				data.evening_is_approximate = body['evening_is_approximate']
			if 'night_is_approximate' in body:
				data.night_is_approximate = body['night_is_approximate']
			if 'description' in body:
				data.description = body['description']
			if 'pra_name' in body:
				data.pra_name = body['pra_name']
			if 'floor' in body:
				data.floor = body['floor']
			if 'local' in body:
				data.local = body['local']
			if 'contact_name' in body:
				data.contact_name = body['contact_name']
			if 'contact_phone_number' in body:
				data.contact_phone_number = body['contact_phone_number']

		return {
			'message': 'building person requiring assistance modified'
		}

	def remove(self, id_building_person_requiring_assistance):
		""" Remove building person requiring assistance

		:param id_building_person_requiring_assistance: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_building_person_requiring_assistance)
			data.is_active = False
			db.commit()

		return {
			'message': 'building person requiring assistance successfully removed'
		}