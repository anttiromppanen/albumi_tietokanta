from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from sqlalchemy import func

from application import app, db
from application.albums.models import Album
from application.albums.forms import AlbumForm, AlbumEditForm

from application.esittajat.models import Esittaja

from application.esittajat_albumit.models import EsittajatAlbumit

@app.route("/albums", methods=["GET"])
@login_required
def albums_index():
    return render_template("albums/list.html", albums = EsittajatAlbumit.get_albums_by_user())

@app.route("/albums/<album_id>/", methods=["GET"])
@login_required
def album_via_id(album_id):
    album = EsittajatAlbumit.get_album_by_id(album_id)

    print(album)
    # tälle joku error-viesti
    #if not album.lisaaja_id == current_user.id:
    #    return redirect(url_for("albums_index"))

    return render_template("albums/edit.html", albumi = album, form = AlbumEditForm())

@app.route("/albums/<album_id>/", methods=["POST"])
@login_required
def album_edit(album_id):
    album = Album.query.get(album_id)
    form = AlbumEditForm(request.form)

    if not form.validate_on_submit():
        return render_template("albums/edit.html", albumi = album, form = form)

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

    esittajanNimi = form.artisti.data.lower()
    albuminNimi = form.nimi.data.lower()
    julkaisuvuosi = form.julkaisuvuosi.data
    tahtien_maara = int(form.tahtien_maara.data)

    loytyykoEsittaja = Esittaja.query.filter_by(nimi = esittajanNimi).first()

    esittaja = Esittaja(esittajanNimi)

    # albumi vaatii esittäjän, lisätään uusi esittäjä, jos None
    if not loytyykoEsittaja:
        db.session().add(esittaja)
        db.session().commit()

    loytyykoEsittaja = Esittaja.query.filter_by(nimi = esittajanNimi).first()

    albumi = Album(albuminNimi, loytyykoEsittaja.id, julkaisuvuosi, tahtien_maara, current_user.id)

    # Albumi lisätään jos None
    loytyykoAlbumi = Album.query.filter(
            Album.nimi == albuminNimi,
            Album.artist_id == loytyykoEsittaja.id
            ).first()

    if not loytyykoAlbumi:
        db.session().add(albumi)
        db.session().commit()

    loytyykoAlbumi = Album.query.filter(
            Album.nimi == albuminNimi,
            Album.artist_id == loytyykoEsittaja.id
            ).first()

    loytyykoEsittajaJaAlbumi = EsittajatAlbumit.query.filter(
            EsittajatAlbumit.albumi_id == loytyykoAlbumi.id,
            EsittajatAlbumit.esittaja_id == loytyykoEsittaja.id,
            EsittajatAlbumit.lisaaja_id == current_user.id
            ).first()

    # Jos artistin albumi on jo lisätty, error ja pysytään formissa
    if not loytyykoEsittajaJaAlbumi:
        esittajaJaAlbumi = EsittajatAlbumit(loytyykoAlbumi.id, loytyykoEsittaja.id, current_user.id)
        db.session().add(esittajaJaAlbumi)
    else:
        return render_template("albums/new.html", form = form, error = "Olet lisännyt jo kyseisen albumin")

    db.session().commit()

    return redirect(url_for("albums_index"))

@app.route("/delete_album/<album_id>")
def album_delete(album_id):
    album = EsittajatAlbumit.query.get(album_id)
    print(album)

    db.session.delete(album)
    db.session.commit()

    return redirect(url_for("albums_index"))
