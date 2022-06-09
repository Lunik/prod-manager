from sqlalchemy import Integer, Column, ForeignKey

from ProdManager import db
from .Event import Event

class IncidentEvent(Event, db.Model):
  incident_id = Column(Integer, ForeignKey('incident.id'), nullable=False)

  def __repr__(self):
    return f"<IncidentEvent '{self.id}'>"
