import uuid
from cause.api.management.core.database import Database
from cause.api.management.core.multilang import MultiLang
from cause.api.management.resturls.base import Base
from ..models.hazardous_material import HazardousMaterial as Table


class HazardousMaterial(Base):
	table_name = 'tbl_hazardous_material'
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'create',
		'DELETE': 'remove',
		'PATCH': '',
	}

	def get(self, id_hazardous_material=None, is_active=None):
		""" Return all information for hazardous material

		:param id_hazardous_material: UUID
		:param is_active: BOOLEAN
		"""
		with Database() as db:
			if id_hazardous_material is None and is_active is None:
				data = db.query(Table).all()
			elif id_hazardous_material is None:
				data = db.query(Table).filter(Table.is_active == is_active).all()
			else:
				data = db.query(Table).get(id_hazardous_material)

		return {
			'data': data
		}


	def create(self, body):
		""" Create a new hazardous material

		:param body: {
			number: STRING,
			name: JSON,
			guide_number: STRING,
			reaction_to_water: BOOLEAN,
			toxic_inhalation_hazard: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'number' not in body or 'name' not in body:
			raise Exception("You need to pass a 'name' and 'number'")

		id_hazardous_material = uuid.uuid4()
		id_language_content = MultiLang.set(body['name'], True)
		guide_number = body['guide_number'] if 'guide_number' in body else None
		reaction_to_water = body['reaction_to_water'] if 'reaction_to_water' in body else False
		toxic_inhalation_hazard = body['toxic_inhalation_hazard'] if 'toxic_inhalation_hazard' in body else False

		with Database() as db:
			db.insert(Table(id_hazardous_material, body['number'], id_language_content,
			                guide_number, reaction_to_water, toxic_inhalation_hazard))
			db.commit()

		return {
			'id_hazardous_material': id_hazardous_material,
			'message': 'hazardous material successfully created'
		}

	def modify(self, body):
		""" Modify a hazardous material

		:param body: {
			id_hazardous_material: UUID,
			number: STRING,
			name: JSON,
			guide_number: STRING,
			reaction_to_water: BOOLEAN,
			toxic_inhalation_hazard: BOOLEAN,
			is_active: BOOLEAN,
		}
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		if 'id_hazardous_material' not in body:
			raise Exception("You need to pass a id_hazardous_material")

		with Database() as db:
			data = db.query(Table).get(body['id_hazardous_material'])

			if 'name' in body:
				data.id_language_content_name = MultiLang.set(body['name'])
			if 'number' in body:
				data.number = body['number']
			if 'guide_number' in body:
				data.guide_number = body['guide_number']
			if 'reaction_to_water' in body:
				data.reaction_to_water = body['reaction_to_water']
			if 'toxic_inhalation_hazard' in body:
				data.toxic_inhalation_hazard = body['toxic_inhalation_hazard']
			if 'is_active' in body:
				data.is_active = body['is_active']

			db.commit()

		return {
			'message': 'hazardous material successfully modified'
		}

	def remove(self, id_hazardous_material):
		""" Remove a hazardous material

		:param id_hazardous_material: UUID
		"""
		if self.has_permission('RightAdmin') is False:
			self.no_access()

		with Database() as db:
			data = db.query(Table).get(id_hazardous_material)
			data.is_active = False
			db.commit()

		return {
			'message': 'hazardous material successfully removed'
		}