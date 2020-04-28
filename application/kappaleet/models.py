from application import db
from application.models import Base

class Kappale(Base):

  __tablename__ = "kappale"

  nimi = db.Column(db.String(144), nullable=False)
  pituus = db.Column(db.Numeric(3, 2), nullable=False)

  album_id = db.Column(db.Integer, db.ForeignKey('albumi.id'), nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey('tili.id'), nullable=False)

  def __init__(self, nimi, pituus, album_id, account_id):
    self.nimi = nimi
    self.pituus = pituus
    self.album_id = album_id
    self.account_id = account_id