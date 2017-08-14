from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Firestation(Base):
	__tablename__ = "tbl_firestation"

	id_firestation = Column(String(36), primary_key=True)
	id_fire_safety_department = Column(String(36))
	station_name = Column(String(36))
	phone_number = Column(String(10))
	fax_number = Column(String(10))
	email = Column(String(70))
	id_building = Column(String(36))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)