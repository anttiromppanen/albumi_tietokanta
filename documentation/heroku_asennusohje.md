# Heroku asennusohje

1. Aja sovelluksen juurikansiossa komento 'heroku config:set HEROKU=1', annetaan sovellukselle tieto, että sovellus on herokussa
2. Lisätään herokuun PostgreSQL-tietokanta komennolla 'heroku addons:add heroku-postgresql:hobby-dev'
3. Avataan komentorivillä yhteys tietokantaan komennolla '\dt'
4. Luodaan käyttäjäluokat 1 (admin), 2 (user) komennoilla 'INSERT INTO User_group (user_group) VALUES (1)' ja 'INSERT INTO User_group (user_group) VALUES (2)'
5. Luodaan admin-käyttäjä komennolla 'INSERT INTO Tili (username, password, user_group) VALUES ("admin", "admin", 1)'