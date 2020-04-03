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
    return render_template("albums/list.html", albums = EsittajatAlbumit.get_albums_by_user())

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

    loytyykoEsittaja = Esittaja.query.filter_by(nimi = esittajanNimi).first()
    loytyykoAlbumi = Album.query.filter_by(nimi = albuminNimi).first()

    esittaja = Esittaja(esittajanNimi)

    if not loytyykoEsittaja:
        db.session().add(esittaja)
        db.session().commit()

    if not loytyykoAlbumi:
        db.session().add(albumi)
        db.session().commit()

    loytyykoEsittaja = Esittaja.query.filter_by(nimi = esittajanNimi).first()
    loytyykoAlbumi = Album.query.filter_by(nimi = albuminNimi).first()

    loytyykoEsittajaJaAlbumi = EsittajatAlbumit.query.filter(
            EsittajatAlbumit.albumi_id == loytyykoAlbumi.id,
            EsittajatAlbumit.esittaja_id == loytyykoEsittaja.id,
            EsittajatAlbumit.lisaaja_id == current_user.id
            ).first()

    if not loytyykoEsittajaJaAlbumi:
        esittajaJaAlbumi = EsittajatAlbumit(loytyykoAlbumi.id, loytyykoEsittaja.id, current_user.id)
        db.session().add(esittajaJaAlbumi)

    db.session().commit()

    return redirect(url_for("albums_index"))

@app.route("/delete_album/<album_id>")
def album_delete(album_id):
    album = EsittajatAlbumit.query.get(album_id)
    print(album)

    db.session.delete(album)
    db.session.commit()

    return redirect(url_for("albums_index"))
