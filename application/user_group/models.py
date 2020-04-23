from application import db
from application.models import Base

class UserGroup(Base):

  __tablename__ = "kayttajaluokka"

  # 1 = admin, 2 = user
  user_group = db.Column(db.Integer, nullable=False)

  def __init__(self, user_group):
    self.user_group = user_group