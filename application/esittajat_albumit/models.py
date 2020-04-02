from application import db
from application.models import Base

from sqlalchemy.sql import text

class EsittajatAlbumit(Base):

    __tablename__ = "esittajat_albumit"

    albumi_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)
    esittaja_id = db.Column(db.Integer, db.ForeignKey("esittaja.id"), nullable=False)
    lisaaja_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)

    def __init__(self, albumi_id, esittaja_id, lisaaja_id):
        self.albumi_id = albumi_id
        self.esittaja_id = esittaja_id
        self.lisaaja_id = lisaaja_id

    @staticmethod
    def tulosta_kayttajan_lisaamat():
        stmt = text("SELECT id, albumi_id FROM EsittajatAlbumit")
        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})

        return response
