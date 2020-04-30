from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, RegisterForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    
    if not form.validate_on_submit():
        return render_template("auth/loginform.html", form = form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()

    if not user:
        return render_template("auth/loginform.html", form = form, error = "Käyttäjänimi tai salasana väärin")

    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/register", methods = ["GET", "POST"])
def auth_register():
    if request.method == "GET":
        return render_template("auth/registerform.html", form = RegisterForm())

    form = RegisterForm(request.form)

    loytyykoUser = User.query.filter_by(username = form.username.data).first()
    if loytyykoUser:
        return render_template("auth/registerform.html", form = form, error = "Käyttäjänimi varattu, valitse uusi")

    loytyykoUserjaPassword = User.query.filter(
        User.username == form.username.data,
        User.password == form.password.data
        )

    if not form.validate_on_submit():
        return render_template("auth/registerform.html", form = form)

    # user_groupiksi tulee 2, eli user
    user = User(form.username.data, form.password.data, 2)
    db.session().add(user)
    db.session().commit()

    return redirect(url_for("auth_login"))
