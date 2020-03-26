from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.albums.models import Album
from application.albums.forms import AlbumForm

@app.route("/albums", methods=["GET"])
def albums_index():
    return render_template("albums/list.html", albums = Album.query.all())

@app.route("/albums/new/")
@login_required
def albums_form():
    return render_template("albums/new.html", form = AlbumForm())

@app.route("/albums/", methods=["POST"])
@login_required
def albums_create():
    form = AlbumForm(request.form)

    nimi = form.nimi.data
    julkaisuvuosi = form.julkaisuvuosi.data
    tahtien_maara = int(form.tahtien_maara.data)

    #if not form.validate():
    #    return render_template("albums/new.html", form = form)

    albumi = Album(nimi, julkaisuvuosi, tahtien_maara)
    albumi.account_id = current_user.id

    db.session().add(albumi)
    db.session().commit()

    return redirect(url_for("albums_index"))
