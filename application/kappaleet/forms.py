from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators

class SongForm(FlaskForm):
  nimi = StringField("Kappaleen nimi", validators=[validators.InputRequired(), validators.Length(min=1, max=100)])
  pituus = DecimalField("Pituus", places=2, rounding=None, validators=[validators.InputRequired(), validators.NumberRange(min=0.1, max=100)])

  class Meta:
      csrf = False