from application import db

class EsittajatAlbumit(db.Model):

    __tablename__ = "esittajat_albumit"

    albumi_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)
    esittaja_id = db.Column(db.Integer, db.ForeignKey("esittaja.id"), nullable=False)

    def __init__(self, albumi_id, esittaja_id):
        self.albumi_id = albumi_id
        self.esittaja_id = esittaja_id
    
