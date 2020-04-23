from flask import render_template
from application import app

from application.esittajat_albumit.models import EsittajatAlbumit

@app.route("/")
def index():
    return render_template("index.html", numOfAlbums = EsittajatAlbumit.get_num_of_albums()[0])
