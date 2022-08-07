from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from ProdManager import db
from ProdManager.helpers.links import custom_url_for

from .Monitor import Monitor

class Scope(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), unique=True, nullable=False)
  description = Column(String(), nullable=True)
  incidents = relationship(
    'Incident',
    backref='scope',
    lazy='dynamic',
  )
  maintenances = relationship(
    'Maintenance',
    backref='scope',
    lazy='dynamic',
  )
  monitors = relationship(
    'Monitor',
    backref='scope',
    lazy='dynamic',
  )

  def __repr__(self):
    return f"<Scope '{self.name}'>"

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
        self=custom_url_for('scope_api.show', resource_id=self.id),
        incidents=custom_url_for('incident_api.list', scope=self.id),
        maintenances=custom_url_for('maintenance_api.list', scope=self.id),
        monitors=custom_url_for('monitor_api.list', scope=self.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return cls.name.asc()

  @property
  def monitors_count(self):
    return Monitor.count_monitors(self.monitors)
