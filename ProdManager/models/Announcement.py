from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum, func
from sqlalchemy import and_

from ProdManager.plugins import db, lang
from ProdManager.helpers.model import ModelEnum
from ProdManager.helpers.links import custom_url_for
from ProdManager.helpers.date import current_date, DATETIME_FORMAT

class AnnouncementLevel(ModelEnum):
  HIGH = 'high'
  MEDIUM = 'medium'
  LOW = 'low'

class Announcement(db.Model):
  id = Column(Integer, primary_key=True)
  name = Column(String(), nullable=False)
  description = Column(String(), nullable=False)
  level = Column(Enum(AnnouncementLevel), nullable=False)
  scope_id = Column(Integer, ForeignKey('scope.id'), nullable=False)
  service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
  creation_date = Column(DateTime(), nullable=False)
  start_date = Column(DateTime(), nullable=False)
  end_date = Column(DateTime(), nullable=False)

  def __repr__(self):
    return f"<Announcement '{self.name}'>"

  @property
  def serialize(self):
    return dict(
      name=self.name,
      description=self.description,
      level=self.level.value,
      scope=self.scope.id,
      service=self.service.id,
      creation_date=self.creation_date,
      start_date=self.start_date,
      end_date=self.end_date,
    )

  @property
  def api_serialize(self):
    return self.serialize | dict(
      id=self.id,
      links=dict(
        self=custom_url_for('announcement_api.show', resource_id=self.id),
        scope=custom_url_for('scope_api.show', resource_id=self.scope.id),
        service=custom_url_for('service_api.show', resource_id=self.service.id),
      ),
    )

  @classmethod
  def default_order(cls):
    return (cls.start_date.desc(), cls.level.asc())

  @classmethod
  def reverse_order(cls):
    return (cls.start_date.desc(), cls.level.asc())

  @classmethod
  def ongoing_filter(cls, raw=False):
    now = current_date().strftime(DATETIME_FORMAT)
    filters = [Announcement.start_date <= now, Announcement.end_date >= now]

    if raw:
      return dict(start_before=now, end_after=now)

    return and_(*filters)

  @classmethod
  def filters(cls):
    return dict(
      level=(cls.level, AnnouncementLevel, 'eq'),
      scope=(cls.scope_id, int, 'eq'),
      service=(cls.service_id, int, 'eq'),
      start_before=(cls.start_date, str, 'le'),
      start_after=(cls.start_date, str, 'ge'),
      end_before=(cls.end_date, str, 'le'),
      end_after=(cls.end_date, str, 'ge'),
    )

  @property
  def title(self):
    result = f"[{lang.get('announcement_level_' + self.level.value)}] {self.name}"

    return result

  @classmethod
  def count_by_level(cls, serialize=False, filters=()):
    result = {level.value if serialize else level: 0 for level in AnnouncementLevel}

    query_result = db.session.query(
      Announcement.level,
      func.count(Announcement.id)
    ).filter(*filters).group_by(Announcement.level).all()

    for level, value in query_result:
      key = level.value if serialize else level
      result[key] = value

    return result
