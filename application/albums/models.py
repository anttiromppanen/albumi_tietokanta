from application import db

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(144), nullable=False)
    julkaisuvuosi = db.Column(db.Integer, nullable=False)
    tahtien_maara = db.Column(db.Integer, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, nimi, julkaisuvuosi, tahtien_maara):
        self.nimi = nimi
        self.julkaisuvuosi = julkaisuvuosi
        self.tahtien_maara = tahtien_maara
