from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from sqlalchemy import func

from application import app, db
from application.albums.models import Album
from application.albums.forms import AlbumForm, AlbumEditForm

# poistoon kuhan lisäys toimii aputaulukolla
from application.esittajat.models import Esittaja 

from application.esittajat_albumit.models import EsittajatAlbumit

@app.route("/albums", methods=["GET"])
@login_required
def albums_index():
    albumitByUserID = Album.query.filter_by(account_id = current_user.id).all()
    return render_template("albums/list.html", albums = albumitByUserID)

@app.route("/albums/<album_id>/", methods=["GET"])
@login_required
def album_via_id(album_id):
    album = Album.query.get(album_id)

    # tälle joku error-viesti
    if not album.account_id == current_user.id:
        return redirect(url_for("albums_index"))

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

    esittajanNimi = form.artisti.data
    albuminNimi = form.nimi.data
    julkaisuvuosi = form.julkaisuvuosi.data
    tahtien_maara = int(form.tahtien_maara.data)

    albumi = Album(albuminNimi, julkaisuvuosi, tahtien_maara)
    albumi.account_id = current_user.id

    onkoAlbumiJoLisatty = Album.query.filter(
            Album.nimi.like(albuminNimi),
            Album.account_id.like(current_user.id)
            ).first()

    onkoEsittajaJoLisatty = Esittaja.query.filter(
            Esittaja.nimi.like(esittajanNimi)
            ).first()

    if not onkoAlbumiJoLisatty:
        db.session().add(albumi)
        db.session().commit()

    if not onkoEsittajaJoLisatty:
        uusiEsittaja = Esittaja(esittajanNimi)
        db.session().add(uusiEsittaja)
        db.session().commit()
        
    albumiID = Album.query.filter_by(nimi = albuminNimi).first().id
    esittajaID = Esittaja.query.filter_by(nimi = esittajanNimi).first().id

    onkoJoLisatty = EsittajatAlbumit.query.filter(
            EsittajatAlbumit.albumi_id.like(albumiID),
            EsittajatAlbumit.esittaja_id.like(esittajaID),
            EsittajatAlbumit.lisaaja_id.like(current_user.id)
            ).first()

    if not onkoJoLisatty:
        uusiEsittajaAlbumi = EsittajatAlbumit(albumiID, esittajaID, current_user.id)

    db.session().add(uusiEsittajaAlbumi)
    db.session().commit()

    return redirect(url_for("albums_index"))

@app.route("/delete_album/<album_id>")
def album_delete(album_id):
    album = Album.query.get(album_id)

    db.session.delete(album)
    db.session.commit()

    return redirect(url_for("albums_index"))
