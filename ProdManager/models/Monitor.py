from sqlalchemy import String, Integer, Column, ForeignKey, Enum

from ProdManager import db
from ProdManager.helpers.model import ModelEnum
from ProdManager.helpers.links import custom_url_for
import ProdManager.helpers.resource as ResourceHelpers

class MonitorStatus(ModelEnum):
  OK = 'ok'
  WARNING = 'warning'
  ALERT = 'alert'


class Monitor(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=True)
  integration = Column(String(), nullable=True)
  external_reference = Column(String(), nullable=True)
  external_link = Column(String(), nullable=True)
  status = Column(Enum(MonitorStatus), nullable=False, default=MonitorStatus.OK)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

  def __repr__(self):
    return f"<Monitor '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      scope=self.scope.id,
      service=self.service.id,
      integration=self.integration,
      external_reference=self.external_reference,
      external_link=self.external_link,
      status=self.status.value,
    )

  @property
  def api_serialize(self):
    return self.serialize | dict(
      id=self.id,
      links=dict(
        self=custom_url_for('monitor_api.show', resource_id=self.id),
        scope=custom_url_for('scope_api.show', resource_id=self.scope.id),
        service=custom_url_for('service_api.show', resource_id=self.service.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return cls.name.asc()

  @classmethod
  def filters(cls):
    return dict(
      status=(cls.status, MonitorStatus, 'eq'),
      scope=(cls.scope_id, int, 'eq'),
      service=(cls.service_id, int, 'eq'),
      integration=(cls.integration, str, 'eq'),
    )

  @classmethod
  def count_by_status(cls, query, serialize=False):
    result = dict()

    for status in MonitorStatus:
      key = status.value if serialize else status
      result[key] = ResourceHelpers.count_in_status_from_query(cls, query, status)

    return result
