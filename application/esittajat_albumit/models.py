from application import db
from application.models import Base

from flask_login import current_user

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
    def get_albums_by_user():
        stmt = text("SELECT Esittaja.nimi, Album.nimi,"
                    " Album.julkaisuvuosi, Album.tahtien_maara,"
                    " Album.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id"
                    " FROM Esittajat_albumit, Esittaja, Album WHERE"
                    " Esittajat_albumit.albumi_id = Album.id AND"
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
        stmt = text("SELECT Esittaja.nimi, Album.nimi,"
                    " Album.julkaisuvuosi, Album.tahtien_maara,"
                    " Album.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id"
                    " FROM Esittajat_albumit, Esittaja, Album WHERE"
                    " Esittajat_albumit.albumi_id = Album.id AND"
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