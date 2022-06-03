from sqlalchemy import Integer, Column, ForeignKey

from ProdManager import db
from .Comment import Comment

class MaintenanceComment(Comment, db.Model):
  maintenance_id = Column(Integer, ForeignKey('maintenance.id'), nullable=False)

  def __repr__(self):
    return f"<MaintenanceComment '{self.id}'>"
