from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager import lang
from ProdManager.helpers.model import ModelEnum

class IncidentSeverity(ModelEnum):
  CRITICAL = 'critical'
  HIGH = 'high'
  MODERATE = 'moderate'
  LOW = 'low'
  MINOR = 'minor'

class IncidentStatus(ModelEnum):
  ACTIVE = 'active'
  INVESTIGATING = 'investigating'
  STABLE = 'stable'
  RESOLVED = 'resolved'

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
  investigation_date = Column(DateTime(), nullable=True)
  stable_date = Column(DateTime(), nullable=True)
  resolve_date = Column(DateTime(), nullable=True)
  events = relationship(
    'IncidentEvent',
    backref='incident',
    lazy='dynamic',
    order_by='desc(IncidentEvent.creation_date)',
    cascade="all, delete",
  )

  def __repr__(self):
    return f"<Incident '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      external_reference=self.external_reference,
      status=self.status.name,
      severity=self.severity.name,
      scope=self.scope.name,
      service=self.service.name,
      creation_date=self.creation_date,
      start_impact_date=self.start_impact_date,
      investigation_date=self.investigation_date,
      stable_date=self.stable_date,
      resolve_date=self.resolve_date,
    )

  @classmethod
  def default_order(cls):
    return (cls.start_impact_date.desc(), cls.status.asc(), cls.severity.asc())

  @classmethod
  def reverse_order(cls):
    return (cls.start_impact_date.asc(), cls.status.asc(), cls.severity.asc())

  @classmethod
  def ongoing_filter(cls):
    return Incident.status.in_([
      IncidentStatus.ACTIVE,
      IncidentStatus.INVESTIGATING,
      IncidentStatus.STABLE,
    ])

  @classmethod
  def past_filter(cls):
    return Incident.status.in_([IncidentStatus.RESOLVED])

  @classmethod
  def filters(cls):
    return [
      ("status", cls.status, IncidentStatus),
      ("severity", cls.severity, IncidentSeverity),
      ("scope", cls.scope_id, int),
      ("service", cls.service_id, int),
    ]

  @property
  def title(self):
    result = f"[{lang.get('incident_severity_' + self.severity.value)}][{lang.get('incident_status_' + self.status.value)}] {self.name}"

    if self.external_reference:
      result = f"[{self.external_reference}]" + result

    return result