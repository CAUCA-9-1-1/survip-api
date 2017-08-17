from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BuildingPersonRequiringAssistance(Base):
	__tablename__ = "tbl_building_person_requiring_assistance"

	id_building_person_requiring_assistance = Column(String(36), primary_key=True, nullable=False)
	id_building = Column(String(36), nullable=False)
	id_person_requiring_assistance_type = Column(String(36), nullable=False)
	day_resident_count = Column(Numeric, nullable=False)
	evening_resident_count = Column(Numeric, nullable=False)
	night_resident_count = Column(Numeric, nullable=False)
	day_is_approximate = Column(Boolean, default=False)
	evening_is_approximate = Column(Boolean, default=False)
	night_is_approximate = Column(Boolean, default=False)
	description = Column(Text)
	pra_name = Column(String(60))
	floor = Column(String(3))
	local = Column(String(3))
	contact_name = Column(String(60))
	contact_phone_number = Column(String(10))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_building_person_requiring_assistance, id_building, id_person_requiring_assistance_type,
	             day_resident_count, evening_resident_count, night_resident_count, day_is_approximate, evening_is_approximate, night_is_approximate,
	             description, pra_name, floor, local, contact_name, contact_phone_number
	             ):
		self.id_building_person_requiring_assistance = id_building_person_requiring_assistance
		self.id_building = id_building
		self.id_person_requiring_assistance_type = id_person_requiring_assistance_type
		self.day_resident_count = day_resident_count
		self.evening_resident_count = evening_resident_count
		self.night_resident_count = night_resident_count
		self.day_is_approximate = day_is_approximate
		self.evening_is_approximate = evening_is_approximate
		self.night_is_approximate = night_is_approximate
		self.description = description
		self.pra_name = pra_name
		self.floor = floor
		self.local = local
		self.contact_name = contact_name
		self.contact_phone_number = contact_phone_number
