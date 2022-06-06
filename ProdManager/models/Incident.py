import enum

from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

from .IncidentComment import IncidentComment

class IncidentSeverity(ModelEnum):
  CRITICAL = 'critical'
  HIGH = 'high'
  MODERATE = 'moderate'
  LOW = 'low'
  MINOR = 'minor'

class IncidentStatus(ModelEnum):
  ACTIVE = 'active'
  STABLE = 'stable'
  RESOLVED = 'resolved'
  COMPLETED = 'completed'

class Incident(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=True)
  external_reference = Column(String(), nullable=True)
  status = Column(Enum(IncidentStatus), nullable=False, default=IncidentStatus.ACTIVE)
  severity = Column(Enum(IncidentSeverity), nullable=False)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
  creation_date = Column(DateTime(), nullable=False)
  start_impact_date = Column(DateTime(), nullable=True)
  resolve_date = Column(DateTime(), nullable=True)
  comments = relationship('IncidentComment', backref='incident', lazy='dynamic', order_by='desc(IncidentComment.creation_date)', cascade="all, delete")

  def __repr__(self):
    return f"<Incident '{self.name}'>"

def filter_ongoing_incident(query, limit=10):
  return query.filter(
    Incident.status.in_([IncidentStatus.ACTIVE, IncidentStatus.STABLE])
  ).limit(limit)

def filter_past_incident(query, limit=10):
  return query.filter(
    Incident.status.in_([IncidentStatus.RESOLVED, IncidentStatus.COMPLETED])
  ).limit(limit)