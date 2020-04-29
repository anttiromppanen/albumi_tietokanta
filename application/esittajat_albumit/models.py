from application import db
from application.models import Base

from flask_login import current_user

from sqlalchemy.sql import text

class EsittajatAlbumit(Base):

    __tablename__ = "esittajat_albumit"

    albumi_id = db.Column(db.Integer, db.ForeignKey("albumi.id"), nullable=False)
    esittaja_id = db.Column(db.Integer, db.ForeignKey("esittaja.id"), nullable=False)
    lisaaja_id = db.Column(db.Integer, db.ForeignKey("tili.id"), nullable=False)

    tahtien_maara = db.Column(db.Integer, nullable=False)

    def __init__(self, albumi_id, esittaja_id, lisaaja_id, tahtien_maara):
        self.albumi_id = albumi_id
        self.esittaja_id = esittaja_id
        self.lisaaja_id = lisaaja_id
        self.tahtien_maara = tahtien_maara

    @staticmethod
    def get_albums_by_user():
        stmt = text("SELECT Esittaja.nimi, Albumi.nimi,"
                    " Albumi.julkaisuvuosi, Esittajat_albumit.tahtien_maara,"
                    " Albumi.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id"
                    " FROM Esittajat_albumit, Esittaja, Albumi WHERE"
                    " Esittajat_albumit.albumi_id = Albumi.id AND"
                    " Esittajat_albumit.esittaja_id = Esittaja.id AND"
                    " lisaaja_id = :user").params(user=current_user.id)

        res = db.engine.execute(stmt)

        result = []
        for row in res:
            result.append({
                "esittaja": row[0],
                "albumi": row[1],
                "julkaisuvuosi": row[2],
                "tahtien_maara": row[3],
                "album_id": row[4],
                "esittajat_albumit_id": row[5],
                "lisaaja_id": row[6]})

        return result

    @staticmethod
    def get_all_albums():
        stmt = text("SELECT Esittaja.nimi, Albumi.nimi,"
                    " Albumi.julkaisuvuosi, Esittajat_albumit.tahtien_maara,"
                    " Albumi.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id"
                    " FROM Esittajat_albumit, Esittaja, Albumi WHERE"
                    " Esittajat_albumit.albumi_id = Albumi.id AND"
                    " Esittajat_albumit.esittaja_id = Esittaja.id")

        res = db.engine.execute(stmt)

        result = []
        for row in res:
            result.append({
                "esittaja": row[0],
                "albumi": row[1],
                "julkaisuvuosi": row[2],
                "tahtien_maara": row[3],
                "album_id": row[4],
                "esittajat_albumit_id": row[5],
                "lisaaja_id": row[6]})

        return result

    @staticmethod
    def get_num_of_albums():
        stmt = text("SELECT COUNT(*), COUNT(DISTINCT lisaaja_id) FROM Esittajat_albumit")

        res = db.engine.execute(stmt)

        result = []
        for row in res:
            result.append({
                "albumien_maara": row[0],
                "lisaajien_maara": row[1]})

        return result