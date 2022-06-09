from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

from .Service import ServiceStatus
from .MaintenanceEvent import MaintenanceEvent

class MaintenanceStatus(ModelEnum):
  SCHEDULED = 'scheduled'
  IN_PROGRESS = 'in-progress'
  SUCCEED = 'succeed'
  FAILED = 'failed'

class Maintenance(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=True)
  external_reference = Column(String(), nullable=True)
  status = Column(Enum(MaintenanceStatus), nullable=False)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
  service_status = Column(Enum(ServiceStatus), nullable=False)
  creation_date = Column(DateTime(), nullable=False)
  scheduled_start_date = Column(DateTime(), nullable=False)
  scheduled_end_date = Column(DateTime(), nullable=False)
  start_date = Column(DateTime(), nullable=True)
  end_date = Column(DateTime(), nullable=True)
  events = relationship(
    'MaintenanceEvent',
    backref='maintenance',
    lazy='dynamic',
    order_by='desc(MaintenanceEvent.creation_date)',
    cascade="all, delete",
  )

  def __repr__(self):
    return f"<Maintenance '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      external_reference=self.external_reference,
      status=self.status.name,
      scope=self.scope.name,
      service=self.service.name,
      service_status=self.service_status.name,
      creation_date=self.creation_date,
      scheduled_start_date=self.scheduled_start_date,
      scheduled_end_date=self.scheduled_end_date,
      start_date=self.start_date,
      end_date=self.end_date,
    )

def filter_ongoing_maintenance(query, limit=10):
  return query.filter(
    Maintenance.status.in_([MaintenanceStatus.SCHEDULED, MaintenanceStatus.IN_PROGRESS])
  ).limit(limit)

def filter_past_maintenance(query, limit=10):
  return query.filter(
    Maintenance.status.in_([MaintenanceStatus.SUCCEED, MaintenanceStatus.FAILED])
  ).limit(limit)
