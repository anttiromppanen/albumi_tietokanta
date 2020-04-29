from application import db
from application.models import Base

from flask_login import current_user

from sqlalchemy.sql import text

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

  @staticmethod
  def get_length_of_all_songs():
    stmt = text("SELECT SUM(pituus) FROM Kappale")

    res = db.engine.execute(stmt)

    result = []
    for row in res:
      result.append({ "pituus": round(row[0], 2) })

    return result

  @staticmethod
  def get_length_of_songs_for_album(album_id):
    stmt = text("SELECT SUM(pituus) FROM Kappale, Albumi, Tili"
                " WHERE Kappale.album_id = :albumi_id AND"
                " Kappale.account_id = Tili.id"
                " GROUP BY Albumi.id").params(albumi_id = album_id)
              
    res = db.engine.execute(stmt)

    result = []
    for row in res:
      result.append({ "pituus": round(row[0], 2) })
    
    return result