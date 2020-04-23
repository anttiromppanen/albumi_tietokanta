from application import db
from application.models import Base

class Album(Base):
    # id ja created_at tulee Basesta
    nimi = db.Column(db.String(144), nullable=False)
    julkaisuvuosi = db.Column(db.Integer, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('esittaja.id'), nullable=False)

    def __init__(self, nimi, artisti_id, julkaisuvuosi, account_id):
        self.nimi = nimi.lower()
        self.artist_id = artisti_id
        self.julkaisuvuosi = julkaisuvuosi
        self.account_id = account_id