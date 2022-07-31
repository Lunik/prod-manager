from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.model import ModelEnum
from ProdManager.helpers.links import custom_url_for

from .Monitor import Monitor

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

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
    )

  @property
  def api_serialize(self):
    return self.serialize | dict(
      id=self.id,
      incidents_count=self.incidents.count(),
      maintenances_count=self.maintenances.count(),
      monitors_count=self.monitors.count(),
      links=dict(
        self=custom_url_for('service_api.show', resource_id=self.id),
        incidents=custom_url_for('incident_api.list', service=self.id),
        maintenances=custom_url_for('maintenance_api.list', service=self.id),
        monitors=custom_url_for('monitor_api.list', service=self.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return cls.name.asc()

  @property
  def monitors_count(self):
    return Monitor.count_monitors(self.monitors)
