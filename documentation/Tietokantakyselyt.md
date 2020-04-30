# Tietokantakyselyt

User:

Kaikkien albumeiden haku:
SELECT Esittaja.nimi, Albumi.nimi, Albumi.julkaisuvuosi, Esittajat_albumit.tahtien_maara, Albumi.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id FROM Esittajat_albumit, Esittaja, Albumi WHERE Esittajat_albumit.albumi_id = Albumi.id AND Esittajat_albumit.esittaja_id = Esittaja.id AND Esittajat_albumit.lisaaja_id = ?

Albumien lisäys:
INSERT INTO esittajat_albumit (created_at, albumi_id, esittaja_id, lisaaja_id, tahtien_maara) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)

Albumin tähtien muokkaus:
UPDATE esittajat_albumit SET tahtien_maara=? WHERE esittajat_albumit.id = ?

Albumin poisto:
DELETE FROM esittajat_albumit WHERE esittajat_albumit.id = ?
DELETE FROM albumi WHERE albumi.id = esittajat_albumit.albumi_id

Yksittäisen albumin näyttäminen:
SELECT kappale.id AS kappale_id, kappale.created_at AS kappale_created_at, kappale.nimi AS kappale_nimi, kappale.pituus AS kappale_pituus, kappale.album_id AS kappale_album_id, kappale.account_id AS kappale_account_id 
FROM kappale 
WHERE kappale.album_id = ?

Kappaleen lisäys:
INSERT INTO kappale (created_at, nimi, pituus, album_id, account_id) VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?)

Kappaleen muokkaus:
UPDATE kappale SET nimi=?, pituus=? WHERE kappale.id = ?

Kappaleen poisto:
DELETE FROM kappale WHERE kappale.id = ?

Admin:

Kaikkien albumeiden haku:
SELECT Esittaja.nimi, Albumi.nimi, Albumi.julkaisuvuosi, Esittajat_albumit.tahtien_maara, Albumi.id, Esittajat_albumit.id, Esittajat_albumit.lisaaja_id FROM Esittajat_albumit, Esittaja, Albumi WHERE Esittajat_albumit.albumi_id = Albumi.id AND Esittajat_albumit.esittaja_id = Esittaja.id