from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[validators.InputRequired(), validators.Length(min=3)])
    password = PasswordField("Salasana", validators=[validators.InputRequired(), validators.Length(min=5)])
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    username = StringField("Käyttäjänimi", validators=[validators.InputRequired(), validators.Length(min=3)])
    password = PasswordField("Salasana", validators=[validators.InputRequired(), validators.Length(min=5)])

    class Meta:
        csrf = False
