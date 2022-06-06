from sqlalchemy import String, Column

from ProdManager import db

class App(db.Model):
  version = Column(String(), primary_key=True)

  def __repr__(self):
    return f"<App {self.version}>"
