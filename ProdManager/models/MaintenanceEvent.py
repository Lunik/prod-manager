from sqlalchemy import Integer, Column, ForeignKey

from ProdManager import db
from .Event import Event

class MaintenanceEvent(Event, db.Model):
  maintenance_id = Column(Integer, ForeignKey('maintenance.id'), nullable=False)

  def __repr__(self):
    return f"<MaintenanceEvent '{self.id}'>"
