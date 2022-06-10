from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship

from ProdManager import db

from .Monitor import count_monitors

class Scope(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), unique=True, nullable=False)
  description = Column(String(), nullable=True)
  incidents = relationship(
    'Incident',
    backref='scope',
    lazy='dynamic',
    order_by="desc(Incident.creation_date)",
  )
  maintenances = relationship(
    'Maintenance',
    backref='scope',
    lazy='dynamic',
    order_by="desc(Maintenance.creation_date)",
  )
  monitors = relationship(
    'Monitor',
    backref='scope',
    lazy='dynamic',
  )

  def __repr__(self):
    return f"<Scope '{self.name}'>"

  @property
  def monitors_count(self):
    return count_monitors(self.monitors)
