import uuid
from cause.api.management.core.database import Database
from cause.api.management.resturls.base import Base

class BuildingHazardousMaterial(Base):
	mapping_method = {
		'GET': 'get',
		'PUT': 'modify',
		'POST': 'assign',
		'DELETE': '',
		'PATCH': '',
	}

	def get(self, id_building):
		""" Return all hazardous material for one building

		:param id_building: UUID
		"""
		with Database() as db:
			data = db.get_all("SELECT * FROM tbl_building_hazardous_material WHERE id_building=%s;", (id_building,))

		return {
			'data': data
		}

	def assign(self, body):
		""" Assign new hazardous material to building

		:param body: {
			id_building: UUID,
			id_hazardous_material: UUID,
			quantity: INTEGER,
			container: STRING,
			capacity_container: STRING,
			id_unit_of_measure: UUID,
			place: STRING,
			floor: STRING,
			gas_inlet: STRING,
			security_perimeter: TEXT,
			other_information: TEXT,
		}
		"""
		with Database() as db:
			db.execute("""INSERT INTO tbl_building_hazardous_material(
							id_building, id_hazardous_material, quantity, container, capacity_container, id_unit_of_measure, place, floor,
							gas_inlet, security_perimeter, other_information, is_active
						  ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, True);""", (
				body['id_building'], body['id_hazardous_material'], body['quantity'], body['container'], body['capacity_container'],
				body['id_unit_of_measure'], body['place'], body['floor'], body['gas_inlet'], body['security_perimeter'],
				body['other_information']
			))

		return {
			'message': 'building hazardous material successfully assigned'
		}

	def modify(self, body):
		""" Modify all information for hazardous material

		:param body: {
			id_building: UUID,
			id_hazardous_material: UUID,
			quantity: INTEGER,
			container: STRING,
			capacity_container: STRING,
			id_unit_of_measure: UUID,
			place: STRING,
			floor: STRING,
			gas_inlet: STRING,
			security_perimeter: TEXT,
			other_information: TEXT,
		}
		"""
		with Database() as db:
			db.execute("""UPDATE tbl_building_hazardous_material SET
							quantity=%s, container=%s, capacity_container=%s, id_unit_of_measure=%s, place=%s, floor=%s,
							gas_inlet=%s, security_perimeter=%s, other_information=%s
						  WHERE id_building=%s and id_hazardous_material=%s;""", (
				body['quantity'], body['container'], body['capacity_container'], body['id_unit_of_measure'], body['place'], body['floor'],
				body['gas_inlet'], body['security_perimeter'], body['other_information'], body['id_building'],
				body['id_hazardous_material']
			))

		return {
			'message': 'building hazardous material successfully modified'
		}