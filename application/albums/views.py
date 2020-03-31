from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from application import app, db
from application.albums.models import Album
from application.albums.forms import AlbumForm, AlbumEditForm

@app.route("/albums", methods=["GET"])
@login_required
def albums_index():
    return render_template("albums/list.html", albums = Album.query.all())

@app.route("/albums/<album_id>/", methods=["GET"])
@login_required
def album_via_id(album_id):
    album = Album.query.get(album_id)
    print(album)

    return render_template("albums/id.html", albumi = album, form = AlbumEditForm())

@app.route("/albums/<album_id>/", methods=["POST"])
@login_required
def album_edit(album_id):
    album = Album.query.get(album_id)
    form = AlbumEditForm(request.form)

    if not form.validate_on_submit():
        return render_template("albums/id.html", albumi = album, form = form)

    album.tahtien_maara = form.tahtien_maara.data
    db.session().commit()

    return redirect(url_for("albums_index"))

@app.route("/albums/new/")
@login_required
def albums_form():
    return render_template("albums/new.html", form = AlbumForm())

@app.route("/albums/", methods=["POST"])
@login_required
def albums_create():
    form = AlbumForm(request.form)

    if not form.validate_on_submit():
        return render_template("albums/new.html", form = form)

    nimi = form.nimi.data
    julkaisuvuosi = form.julkaisuvuosi.data
    tahtien_maara = int(form.tahtien_maara.data)

    albumi = Album(nimi, julkaisuvuosi, tahtien_maara)
    albumi.account_id = current_user.id

    db.session().add(albumi)
    db.session().commit()

    return redirect(url_for("albums_index"))
