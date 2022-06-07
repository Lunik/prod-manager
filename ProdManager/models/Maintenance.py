import enum

from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

from .Service import ServiceStatus
from .MaintenanceComment import MaintenanceComment

class MaintenanceStatus(ModelEnum):
  CREATED = 'created'
  VALIDATED = 'validated'
  SHEDULED = 'sheduled'
  IN_PROGRESS = 'in-progress'
  SUCCESS = 'success'
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
  scheduled_start_date = Column(DateTime(), nullable=True)
  scheduled_end_date = Column(DateTime(), nullable=True)
  start_date = Column(DateTime(), nullable=True)
  end_date = Column(DateTime(), nullable=True)
  comments = relationship('MaintenanceComment', backref='maintenance', lazy='dynamic', order_by='desc(MaintenanceComment.creation_date)', cascade="all, delete")

  def __repr__(self):
    return f"<Maintenance '{self.name}'>"

def filter_ongoing_maintenance(query, limit=10):
  return query.filter(
    Maintenance.status.in_([MaintenanceStatus.SHEDULED, MaintenanceStatus.IN_PROGRESS])
  ).limit(limit)

def filter_past_maintenance(query, limit=10):
  return query.filter(
    Maintenance.status.in_([MaintenanceStatus.SUCCESS, MaintenanceStatus.FAILED])
  ).limit(limit)