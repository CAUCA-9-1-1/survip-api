import json
from datetime import datetime

from geoalchemy2 import Geometry, functions
from sqlalchemy import Column, Boolean, DateTime, Float, String, Text, ForeignKey, SMALLINT, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from cause.api.management.core.database import Database
from .fire_hydrant_type import FireHydrantType
from .intersection import Intersection
from .lane import Lane


Base = declarative_base()


class InterventionPlanCourseLane(Base):
	__tablename__ = "tbl_intervention_plan_course_lane"

	id_intervention_plan_course_lane = Column(String(36), primary_key=True)
	id_intervention_plan_course = Column(String(36))
	id_lane = Column(String(36), ForeignKey(Lane.id_lane))
	direction = Column(SMALLINT)
	sequence = Column(Integer)
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	def __init__(self, id_intervention_plan_course_lane, id_intervention_plan_course, id_lane, direction, sequence):
		self.id_intervention_plan_course_lane = id_intervention_plan_course_lane
		self.id_intervention_plan_course = id_intervention_plan_course
		self.direction = direction
		self.sequence = sequence
		self.id_lane = id_lane
