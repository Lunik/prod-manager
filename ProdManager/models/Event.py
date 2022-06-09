import json
from sqlalchemy import String, Integer, Column, DateTime, Enum

from ProdManager.helpers.model import ModelEnum

class EventType(ModelEnum):
  CREATE = 'create'
  UPDATE = 'update'
  COMMENT = 'comment'

class Event:
  id = Column(Integer, primary_key=True)
  creation_date = Column(DateTime(), nullable=False)
  type = Column(Enum(EventType), nullable=False)
  content = Column(String(), nullable=False)

  def __repr__(self):
    return f"<Event '{self.id}'>"

  def get_content(self):
    if self.type in [EventType.CREATE, EventType.UPDATE]:
      return json.loads(self.content)

    return self.content
