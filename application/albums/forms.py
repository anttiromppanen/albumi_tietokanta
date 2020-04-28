from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, DecimalField, validators

from datetime import datetime

class AlbumForm(FlaskForm):
    artisti = StringField("Artisti", validators=[validators.InputRequired(), validators.Length(min=1, max=100)])
    nimi = StringField("Albumin nimi", validators=[validators.InputRequired(), validators.Length(min=2, max=100)])
    julkaisuvuosi = IntegerField("Julkaisuvuosi", validators=[validators.InputRequired(), validators.NumberRange(min=1500, max=datetime.now().year)])
    tahtien_maara = RadioField("Tähtien määrä", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")], default="1", validators=[validators.InputRequired()])

    class Meta:
        csrf = False

class AlbumEditForm(FlaskForm):
    tahtien_maara = RadioField("Tähtien määrä", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")], default="1", validators=[validators.InputRequired()])

    class Meta:
        csrf = False

class AddSongForm(FlaskForm):
    nimi = StringField("Kappaleen nimi", validators=[validators.InputRequired(), validators.Length(min=1, max=100)])
    pituus = DecimalField("Pituus", places=2, rounding=None, validators=[validators.InputRequired(), validators.Length(min=0.1, max=100)])

    class Meta:
        csrf = False