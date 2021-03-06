from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from sqlalchemy import func

from application import app, db
from application.albums.models import Albumi
from application.albums.forms import AlbumForm, AlbumEditForm, AddSongForm

from application.esittajat.models import Esittaja

from application.kappaleet.models import Kappale
from application.kappaleet.forms import SongForm

from application.esittajat_albumit.models import EsittajatAlbumit

@app.route("/albums", methods=["GET"])
@login_required
def albums_index():
    if current_user.user_group == 1:
        return render_template("albums/list.html", albums = EsittajatAlbumit.get_all_albums(), albums_and_songs = EsittajatAlbumit.get_num_of_albums_and_songs_for_admin()[0])

    return render_template("albums/list.html", albums = EsittajatAlbumit.get_albums_by_user(), albums_and_songs = EsittajatAlbumit.get_num_of_albums_and_songs_by_user()[0])

@app.route("/albums/<album_id>/", methods=["GET"])
@login_required
def album_view_id(album_id):
    if current_user.user_group == 1:
        esittajaJaAlbumi = EsittajatAlbumit.query.filter(
            EsittajatAlbumit.albumi_id == album_id
            ).first() 

        albumi = Albumi.query.filter_by(id = esittajaJaAlbumi.albumi_id).first()
        esittaja = Esittaja.query.filter_by(id = esittajaJaAlbumi.esittaja_id).first()

        kappaleet = Kappale.query.filter_by(album_id = albumi.id).all()
        print("------------------------")
        print(kappaleet)
        print("------------------------")

        return render_template("albums/view.html", albumi = albumi, esittaja = esittaja, kappaleet = kappaleet, form = SongForm(), sums_length = Kappale.get_length_of_songs_for_album(albumi.id))

    esittajaJaAlbumi = EsittajatAlbumit.query.filter(
        EsittajatAlbumit.albumi_id == album_id,
        EsittajatAlbumit.lisaaja_id == current_user.id
        ).first()

    albumi = Albumi.query.filter_by(id = esittajaJaAlbumi.albumi_id).first()
    esittaja = Esittaja.query.filter_by(id = esittajaJaAlbumi.esittaja_id).first()

    kappaleet = Kappale.query.filter_by(album_id = albumi.id).all()
    print("------------------------")
    print(kappaleet)
    print("------------------------")

    return render_template("albums/view.html", albumi = albumi, esittaja = esittaja, kappaleet = kappaleet, form = SongForm(), sums_length = Kappale.get_length_of_songs_for_album(albumi.id))

@app.route("/albums/<album_id>/", methods=["POST"])
@login_required
def post_new_song(album_id):
    form = AddSongForm(request.form)

    kappaleenNimi = form.nimi.data
    kappaleenPituus = form.pituus.data
    albumi = Albumi.query.filter_by(id = album_id).first()
    kayttaja = current_user

    if not form.validate_on_submit():
        esittaja = Esittaja.query.filter_by(id = albumi.artist_id).first()
        kappaleet = Kappale.query.filter_by(album_id = albumi.id).all()
        print(form.pituus.errors)
        return render_template("albums/view.html", albumi = albumi, esittaja = esittaja, kappaleet = kappaleet, form = form)

    print("------------------------")
    print(form.nimi.data)
    print(form.pituus.data)
    print(albumi, albumi.nimi)
    print("Käyttäjä: ", kayttaja)
    print("------------------------")

    kappale = Kappale(kappaleenNimi, kappaleenPituus, albumi.id, kayttaja.id)

    db.session().add(kappale)
    db.session().commit()

    return redirect(url_for("album_view_id", album_id = album_id))

@app.route("/albums/edit/<album_id>/", methods=["GET"])
@login_required
def album_via_id(album_id):
    # Näytetään kaikki albumit, jos käyttäjä on admin
    if current_user.user_group == 1:
        esittajaJaAlbumi = EsittajatAlbumit.query.filter(
        EsittajatAlbumit.albumi_id == album_id
        ).first()

        esittaja = Esittaja.query.filter_by(id = esittajaJaAlbumi.esittaja_id).first()
        albumi = Albumi.query.filter_by(id = esittajaJaAlbumi.albumi_id).first()

        return render_template("albums/edit.html", esittaja = esittaja, albumi = albumi, form = AlbumEditForm())

    # Käyttäjä ei ollut admin, näytetään käyttäjän x lisäämät albumit
    esittajaJaAlbumi = EsittajatAlbumit.query.filter(
        EsittajatAlbumit.albumi_id == album_id,
        EsittajatAlbumit.lisaaja_id == current_user.id
        ).first()
        
    esittaja = Esittaja.query.filter_by(id = esittajaJaAlbumi.esittaja_id).first()
    albumi = Albumi.query.filter_by(id = esittajaJaAlbumi.albumi_id).first()
    
    # tälle joku error-viesti
    if not esittajaJaAlbumi.lisaaja_id == current_user.id:
        return redirect(url_for("albums_index"))

    return render_template("albums/edit.html", esittaja = esittaja, albumi = albumi, form = AlbumEditForm())

@app.route("/albums/edit/<album_id>/", methods=["POST"])
@login_required
def album_edit(album_id):
    album = Albumi.query.get(album_id)
    form = AlbumEditForm(request.form)

    esittajaAlbumi = EsittajatAlbumit.query.filter(
        EsittajatAlbumit.albumi_id == album.id,
        EsittajatAlbumit.lisaaja_id == album.account_id
        ).first()

    if not form.validate_on_submit():
        return render_template("albums/edit.html", albumi = album, form = form)

    esittajaAlbumi.tahtien_maara = form.tahtien_maara.data
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

    albumi = Albumi(albuminNimi, loytyykoEsittaja.id, julkaisuvuosi, current_user.id)

    # Albumi lisätään jos None
    loytyykoAlbumi = Albumi.query.filter(
            Albumi.nimi == albuminNimi,
            Albumi.artist_id == loytyykoEsittaja.id
            ).first()

    if not loytyykoAlbumi:
        db.session().add(albumi)
        db.session().commit()

    loytyykoAlbumi = Albumi.query.filter(
            Albumi.nimi == albuminNimi,
            Albumi.artist_id == loytyykoEsittaja.id
            ).first()

    loytyykoEsittajaJaAlbumi = EsittajatAlbumit.query.filter(
            EsittajatAlbumit.albumi_id == loytyykoAlbumi.id,
            EsittajatAlbumit.esittaja_id == loytyykoEsittaja.id,
            EsittajatAlbumit.lisaaja_id == current_user.id
            ).first()

    # Jos artistin albumi on jo lisätty, error ja pysytään formissa
    if not loytyykoEsittajaJaAlbumi:
        esittajaJaAlbumi = EsittajatAlbumit(loytyykoAlbumi.id, loytyykoEsittaja.id, current_user.id, tahtien_maara) 
        db.session().add(esittajaJaAlbumi)
    else:
        return render_template("albums/new.html", form = form, error = "Olet lisännyt jo kyseisen albumin")

    db.session().commit()

    return redirect(url_for("albums_index"))

@app.route("/delete_album/<album_id>")
def album_delete(album_id):
    album = EsittajatAlbumit.query.get(album_id)
    print(album)

    kappaleet = Kappale.query.filter(Kappale.album_id == album.albumi_id).all()
    for kappale in kappaleet:
        db.session.delete(kappale)
    
    db.session.delete(album)
    db.session.commit()

    return redirect(url_for("albums_index"))
