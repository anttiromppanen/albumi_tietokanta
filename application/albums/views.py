from flask import redirect, render_template, request, url_for

from application import app, db
from application.albums.models import Album
from application.albums.forms import TaskForm

@app.route("/albums", methods=["GET"])
def albums_index():
    return render_template("albums/list.html", albums = Album.query.all())

@app.route("/albums/new/")
def albums_form():
    return render_template("albums/new.html", form = TaskForm())

@app.route("/albums/", methods=["POST"])
def albums_create():
    a = Album(request.form.get("nimi"), request.form.get("julkaisuvuosi"), request.form.get("tahtien_maara"))
    db.session().add(a)
    db.session().commit()

    return redirect(url_for("albums_index"))
