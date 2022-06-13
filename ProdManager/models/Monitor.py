from sqlalchemy import String, Integer, Column, ForeignKey, Enum

from ProdManager import db
from ProdManager.helpers.model import ModelEnum

class MonitorStatus(ModelEnum):
  OK = 'ok'
  WARNING = 'warning'
  ALERT = 'alert'


class Monitor(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=True)
  external_link = Column(String(), nullable=True)
  status = Column(Enum(MonitorStatus), nullable=False, default=MonitorStatus.OK)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

  def __repr__(self):
    return f"<Monitor '{self.name}'>"

  @classmethod
  def default_order(cls):
    return cls.name.asc()


def count_monitors_in_status(query, status):
  return query.filter(
    Monitor.status == status
  ).count()

def count_monitors(query):
  result = dict()

  for status in MonitorStatus:
    result[status] = count_monitors_in_status(query, status)

  return result
