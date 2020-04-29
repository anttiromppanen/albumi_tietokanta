from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user

from sqlalchemy import func

from application import app, db
from application.kappaleet.models import Kappale
from application.kappaleet.forms import SongForm

from application.albums.models import Albumi

from application.esittajat.models import Esittaja

@app.route("/songs/<song_id>/")
@login_required
def delete_song(song_id):
  kappale = Kappale.query.filter_by(id = song_id).first()
  albumi = Albumi.query.filter_by(id = kappale.album_id).first()

  db.session().delete(kappale)
  db.session().commit()

  return redirect(url_for("album_view_id", album_id = albumi.id))

@app.route("/songs/<song_id>/", methods=["POST"])
@login_required
def edit_song(song_id):
  form = SongForm(request.form)
  kappale = Kappale.query.filter_by(id = song_id).first()
  albumi = Albumi.query.filter_by(id = kappale.album_id).first()
  esittaja = Esittaja.query.filter_by(id = albumi.artist_id).first()
  kappaleet = Kappale.query.filter_by(album_id = albumi.id).all()

  print('-------------------')
  print(kappale)
  print(albumi)
  print(form.nimi.data, form.pituus.data)
  print('-------------------')

  if not form.validate_on_submit():
    form.nimi.data = ""
    form.pituus.data = ""
    return render_template("albums/view.html", albumi = albumi, esittaja = esittaja, kappaleet = kappaleet, form = form)

  kappale.nimi = form.nimi.data
  kappale.pituus = form.pituus.data

  db.session().commit()

  return redirect(url_for("album_view_id", album_id = albumi.id))