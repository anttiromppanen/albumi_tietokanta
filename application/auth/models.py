from application import db
from application.models import Base

class User(Base):

    __tablename__ = "account"

    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    albums = db.relationship("Album", backref='account', lazy=True)
    user_group = db.Column(db.Integer, db.ForeignKey('user_group.id'), nullable=False)

    def __init__(self, username, password, user_group):
        self.username = username.lower()
        self.password = password
        self.user_group = user_group
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return self.user_group