from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

from .Monitor import count_monitors

class ServiceStatus(ModelEnum):
  UP = 'up'
  DEGRADED = 'degraded'
  DOWN = 'down'

class Service(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), unique=True, nullable=False)
  description = Column(String(), nullable=True)
  incidents = relationship(
    'Incident',
    backref='service',
    lazy='dynamic',
  )
  maintenances = relationship(
    'Maintenance',
    backref='service',
    lazy='dynamic',
  )
  monitors = relationship(
    'Monitor',
    backref='service',
    lazy='dynamic',
  )

  def __repr__(self):
    return f"<Service '{self.name}'>"

  @classmethod
  def default_order(cls):
    return cls.name.asc()

  @property
  def monitors_count(self):
    return count_monitors(self.monitors)
