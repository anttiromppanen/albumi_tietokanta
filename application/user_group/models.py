from application import db
from application.models import Base

class UserGroup(Base):

  __tablename__ = "user_group"

  # 1 = admin, 2 = user
  group = db.Column(db.Integer, nullable=False)

  def __init__(self, group):
    self.group = group