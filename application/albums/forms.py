from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField, validators

class AlbumForm(FlaskForm):
    nimi = StringField("Album name", validators=[validators.InputRequired(), validators.Length(min=2)])
    julkaisuvuosi = IntegerField("Julkaisuvuosi", validators=[validators.InputRequired()])
    tahtien_maara = RadioField("Tähtien määrä", choices=[("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")], default="1", validators=[validators.InputRequired()])

    class Meta:
        csrf = False
