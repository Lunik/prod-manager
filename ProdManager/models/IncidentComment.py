from sqlalchemy import Integer, Column, ForeignKey

from ProdManager import db
from .Comment import Comment

class IncidentComment(Comment, db.Model):
  incident_id = Column(Integer, ForeignKey('incident.id'), nullable=False)

  def __repr__(self):
    return f"<IncidentComment '{self.id}'>"
