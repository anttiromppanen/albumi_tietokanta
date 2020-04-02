from flask import render_template
from application import app

from application.esittajat_albumit.models import EsittajatAlbumit

@app.route("/")
def index():
    return render_template("index.html", need_albums=EsittajatAlbumit.tulosta_kayttajan_lisaamat)
