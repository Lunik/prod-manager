from sqlalchemy import String, Integer, Column

from ProdManager import db

class Subscriber(db.Model):
  id = Column(Integer, primary_key=True)
  email = Column(String(), unique=True, nullable=False)

  def __repr__(self):
    return f"<Subscriber '{self.email}'>"

  @classmethod
  def default_order(cls):
    return cls.email.asc()
