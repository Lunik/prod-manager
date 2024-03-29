from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship

from flask import g

from ProdManager.plugins import db, lang
from ProdManager.helpers.model import ModelEnum
from ProdManager.helpers.links import custom_url_for

from .IncidentEvent import IncidentEvent

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
  external_reference = Column(String(), nullable=True, index=True)
  status = Column(Enum(IncidentStatus), nullable=False, default=IncidentStatus.ACTIVE)
  severity = Column(Enum(IncidentSeverity), nullable=False)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
  creation_date = Column(DateTime(), nullable=False)
  start_impact_date = Column(DateTime(), nullable=True)
  investigation_date = Column(DateTime(), nullable=True)
  stable_date = Column(DateTime(), nullable=True)
  resolve_date = Column(DateTime(), nullable=True)
  external_link = Column(String(), nullable=True)
  events = relationship(
    'IncidentEvent',
    backref='incident',
    lazy='dynamic',
    order_by='desc(IncidentEvent.creation_date)',
    cascade="all, delete",
  )

  event_type = IncidentEvent

  notify_attributs = ['status']

  def __repr__(self):
    return f"<Incident '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      external_reference=self.external_reference,
      external_link=self.external_link,
      status=self.status.value,
      severity=self.severity.value,
      scope=self.scope.id,
      service=self.service.id,
      creation_date=self.creation_date,
      start_impact_date=self.start_impact_date,
      investigation_date=self.investigation_date,
      stable_date=self.stable_date,
      resolve_date=self.resolve_date,
    )

  @property
  def api_serialize(self):
    if g.logged:
      events = self.events
    else:
      events = self.events.filter(IncidentEvent.internal is False)

    return self.serialize | dict(
      id=self.id,
      events=[event.api_serialize for event in events],
      links=dict(
        self=custom_url_for('incident_api.show', resource_id=self.id),
        scope=custom_url_for('scope_api.show', resource_id=self.scope.id),
        service=custom_url_for('service_api.show', resource_id=self.service.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return (cls.start_impact_date.desc(), cls.status.asc(), cls.severity.asc())

  @classmethod
  def reverse_order(cls):
    return (cls.start_impact_date.asc(), cls.status.asc(), cls.severity.asc())

  @classmethod
  def ongoing_filter(cls, raw=False):
    filters = [
      IncidentStatus.ACTIVE,
      IncidentStatus.INVESTIGATING,
      IncidentStatus.STABLE,
    ]

    if raw:
      return [status.value for status in filters]

    return Incident.status.in_(filters)

  @classmethod
  def past_filter(cls, raw=False):
    filters = [IncidentStatus.RESOLVED]

    if raw:
      return [status.value for status in filters]

    return Incident.status.in_(filters)

  @classmethod
  def filters(cls):
    return dict(
      status=(cls.status, IncidentStatus, 'eq'),
      severity=(cls.severity, IncidentSeverity, 'eq'),
      scope=(cls.scope_id, int, 'eq'),
      service=(cls.service_id, int, 'eq'),
      external_reference=(cls.external_reference, str, 'eq'),
      impact_before=(cls.start_impact_date, str, 'le'),
      impact_after=(cls.start_impact_date, str, 'ge'),
    )

  @property
  def title(self):
    result = f"[{lang.get('incident_severity_' + self.severity.value)}][{lang.get('incident_status_' + self.status.value)}] {self.name}"

    if self.external_reference:
      result = f"[{self.external_reference}]" + result

    return result

  @classmethod
  def count_by_status(cls, serialize=False, filters=()):
    result = {status.value if serialize else status: 0 for status in IncidentStatus}

    query_result = db.session.query(
      Incident.status,
      func.count(Incident.id)
    ).filter(*filters).group_by(Incident.status).all()

    for status, value in query_result:
      key = status.value if serialize else status
      result[key] = value

    return result

  def notify_attachments(self):
    return []
