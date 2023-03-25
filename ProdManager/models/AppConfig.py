from sqlalchemy import String, Integer, Column

from ProdManager.plugins import db

class AppConfig(db.Model):
  id = Column(Integer, primary_key=True)
  uuid = Column(String(), unique=True, nullable=False)

  def __repr__(self):
    return f"<AppConfig '{self.uuid}'>"

  @property
  def serialize(self):
    return dict(
      uuid=self.uuid,
    )

  @property
  def api_serialize(self):
    return self.serialize | dict(
      id=self.id,
    )

  @classmethod
  def default_order(cls):
    return cls.uuid.asc()
