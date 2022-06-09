from sqlalchemy import String, Integer, Column, Enum
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

class ServiceStatus(ModelEnum):
  UP = 'up'
  DEGRADED = 'degraded'
  DOWN = 'down'

class Service(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), unique=True, nullable=False)
  description = Column(String(), nullable=True)
  status = Column(Enum(ServiceStatus), nullable=False, default=ServiceStatus.UP)
  incidents = relationship(
    'Incident',
    backref='service',
    lazy='dynamic',
    order_by='desc(Incident.creation_date)'
  )
  maintenances = relationship(
    'Maintenance',
    backref='service',
    lazy='dynamic',
    order_by='desc(Maintenance.creation_date)'
  )

  def __repr__(self):
    return f"<Service '{self.name}'>"
