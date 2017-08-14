from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from .lane import Lane
from ..models.firestation import Firestation


Base = declarative_base()


class InterventionPlanCourse(Base):
	__tablename__ = "tbl_intervention_plan_course"

	id_intervention_plan_course = Column(String(36), primary_key=True)
	id_intervention_plan = Column(String(36), ForeignKey(Lane.id_lane))
	id_firestation = Column(String(36), ForeignKey(Firestation.id_firestation))
	created_on = Column(DateTime, default=datetime.now)
	is_active = Column(Boolean, default=True)

	firestation = relation(Firestation)

	def __init__(self, id_intervention_plan_course, id_intervention_plan, id_firestation):
		self.id_intervention_plan_course = id_intervention_plan_course
		self.id_intervention_plan = id_intervention_plan
		self.id_firestation = id_firestation
