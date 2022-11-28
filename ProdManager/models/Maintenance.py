from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum, func
from sqlalchemy.orm import relationship

from flask import g

from ProdManager.plugins import db, lang
from ProdManager.helpers.model import ModelEnum
from ProdManager.helpers.links import custom_url_for

from .Service import ServiceStatus
from .MaintenanceEvent import MaintenanceEvent

class MaintenanceStatus(ModelEnum):
  SCHEDULED = 'scheduled'
  IN_PROGRESS = 'in-progress'
  SUCCEED = 'succeed'
  FAILED = 'failed'
  CANCELED = 'canceled'

class Maintenance(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=True)
  external_reference = Column(String(), nullable=True, index=True)
  status = Column(Enum(MaintenanceStatus), nullable=False, default=MaintenanceStatus.SCHEDULED)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
  service_status = Column(Enum(ServiceStatus), nullable=False)
  creation_date = Column(DateTime(), nullable=False)
  scheduled_start_date = Column(DateTime(), nullable=False)
  scheduled_end_date = Column(DateTime(), nullable=False)
  start_date = Column(DateTime(), nullable=True)
  end_date = Column(DateTime(), nullable=True)
  external_link = Column(String(), nullable=True)
  events = relationship(
    'MaintenanceEvent',
    backref='maintenance',
    lazy='dynamic',
    order_by='desc(MaintenanceEvent.creation_date)',
    cascade="all, delete",
  )

  event_type = MaintenanceEvent

  notify_attributs = ['status']

  def __repr__(self):
    return f"<Maintenance '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      external_reference=self.external_reference,
      external_link=self.external_link,
      status=self.status.value,
      scope=self.scope.id,
      service=self.service.id,
      service_status=self.service_status.value,
      creation_date=self.creation_date,
      scheduled_start_date=self.scheduled_start_date,
      scheduled_end_date=self.scheduled_end_date,
      start_date=self.start_date,
      end_date=self.end_date,
    )

  @property
  def api_serialize(self):
    if g.logged:
      events = self.events
    else:
      events = self.events.filter(MaintenanceEvent.internal is False)

    return self.serialize | dict(
      id=self.id,
      events=[event.api_serialize for event in events],
      links=dict(
        self=custom_url_for('maintenance_api.show', resource_id=self.id),
        scope=custom_url_for('scope_api.show', resource_id=self.scope.id),
        service=custom_url_for('service_api.show', resource_id=self.service.id),
        calendar=custom_url_for('maintenance.calendar', resource_id=self.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return (cls.scheduled_start_date.desc(), cls.status.asc())

  @classmethod
  def reverse_order(cls):
    return (cls.scheduled_start_date.asc(), cls.status.asc())

  @classmethod
  def scheduled_filter(cls, raw=False):
    filters = [MaintenanceStatus.SCHEDULED]

    if raw:
      return [status.value for status in filters]

    return Maintenance.status.in_(filters)

  @classmethod
  def ongoing_filter(cls, raw=False):
    filters = [MaintenanceStatus.IN_PROGRESS]

    if raw:
      return [status.value for status in filters]

    return Maintenance.status.in_(filters)

  @classmethod
  def past_filter(cls, raw=False):
    filters = [
      MaintenanceStatus.SUCCEED,
      MaintenanceStatus.FAILED,
      MaintenanceStatus.CANCELED
    ]

    if raw:
      return [status.value for status in filters]

    return Maintenance.status.in_(filters)

  @classmethod
  def filters(cls):
    return dict(
      status=(cls.status, MaintenanceStatus, 'eq'),
      scope=(cls.scope_id, int, 'eq'),
      service=(cls.service_id, int, 'eq'),
      service_status=(cls.service_status, ServiceStatus, 'eq'),
      external_reference=(cls.external_reference, str, 'eq'),
      start_before=(cls.scheduled_start_date, str, 'le'),
      start_after=(cls.scheduled_start_date, str, 'ge'),
      end_before=(cls.scheduled_end_date, str, 'le'),
      end_after=(cls.scheduled_end_date, str, 'ge'),
    )

  @property
  def title(self):
    result = f"[{lang.get('maintenance_status_' + self.status.value)}] {self.name}"

    if self.external_reference:
      result = f"[{self.external_reference}]" + result

    return result

  @classmethod
  def count_by_status(cls, serialize=False, filters=()):
    result = {status.value if serialize else status: 0 for status in MaintenanceStatus}

    query_result = db.session.query(
      Maintenance.status,
      func.count(Maintenance.id)
    ).filter(*filters).group_by(Maintenance.status).all()

    for status, value in query_result:
      key = status.value if serialize else status
      result[key] = value

    return result
