from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, validators

class AlbumForm(FlaskForm):
    nimi = StringField("Album name")
    julkaisuvuosi = IntegerField("Julkaisuvuosi")
    tahtien_maara = RadioField("Tähtien määrä", choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])

    class Meta:
        csrf = False
