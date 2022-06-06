from sqlalchemy import String, Integer, Column, DateTime

class Comment:
  id = Column(Integer, primary_key=True)
  creation_date = Column(DateTime(), nullable=False)
  content = Column(String(), nullable=False)

  def __repr__(self):
    return f"<Comment '{self.id}'>"
