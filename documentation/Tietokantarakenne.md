# Tietokantarakenne

CREATE TABLE esittaja (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	nimi VARCHAR(144) NOT NULL, 
	PRIMARY KEY (id)
)

CREATE TABLE kayttajaluokka (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	user_group INTEGER NOT NULL, 
	PRIMARY KEY (id)
)

CREATE TABLE tili (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	username VARCHAR(144) NOT NULL, 
	password VARCHAR(144) NOT NULL, 
	user_group INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_group) REFERENCES kayttajaluokka (id)
)

CREATE TABLE albumi (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	nimi VARCHAR(144) NOT NULL, 
	julkaisuvuosi INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	artist_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(account_id) REFERENCES tili (id), 
	FOREIGN KEY(artist_id) REFERENCES esittaja (id)
)

CREATE TABLE esittajat_albumit (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	albumi_id INTEGER NOT NULL, 
	esittaja_id INTEGER NOT NULL, 
	lisaaja_id INTEGER NOT NULL, 
	tahtien_maara INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(albumi_id) REFERENCES albumi (id), 
	FOREIGN KEY(esittaja_id) REFERENCES esittaja (id), 
	FOREIGN KEY(lisaaja_id) REFERENCES tili (id)
)

CREATE TABLE kappale (
	id INTEGER NOT NULL, 
	created_at DATETIME, 
	nimi VARCHAR(144) NOT NULL, 
	pituus NUMERIC(3, 2) NOT NULL, 
	album_id INTEGER NOT NULL, 
	account_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(album_id) REFERENCES albumi (id), 
	FOREIGN KEY(account_id) REFERENCES tili (id)
)
