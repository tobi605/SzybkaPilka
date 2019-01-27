BEGIN TRANSACTION;
DELETE FROM `Osoba`;
DELETE FROM `Zawodnik`;
DELETE FROM `Wniosek`;
DELETE FROM `TworzySklad`;
DELETE FROM `Trener`;
DELETE FROM `Sklad`;
DELETE FROM `Sedzia`;
DELETE FROM `Druzyna`;
DELETE FROM `ZarzadcaLigi`;
DELETE FROM `WniosekDruzynowy`;
DELETE FROM `WniosekSkladowy`;

-- admins
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Zarządzac','Ligi','admin@wp.pl','f15e8f09','99cb427eb810ad3787b978b8b6490a7e2f4659925386ba084dd9cbf39555d1ad');
INSERT INTO `ZarzadcaLigi` (email) VALUES ('admin@wp.pl');

-- referees
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Sędzia','Sędzialski','referee@wp.pl','eacfb9ab','6b8caab75903d85f20d50341f3fc8c631ee2b51364678f63f64f2ade2a3686b1');
INSERT INTO `Sedzia` (email) VALUES ('referee@wp.pl');

-- coaches
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Zbyszek','Zbyszek','trener@wp.pl','cb748e73','03da98f8d365b0808b813942ab2daf7f504209247d0203b930bdca80a95ff245');
INSERT INTO `Trener` (email,numerTelefonu) VALUES ('trener@wp.pl',NULL);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Trener','TenDrugi','trener1@wp.pl','226d8716','c4ab2fccb06851820fa274568bd839aa4ad30dc1275a366f78e160d530f9ac34');
INSERT INTO `Trener` (email,numerTelefonu) VALUES ('trener1@wp.pl',NULL);

-- teams
INSERT INTO `Druzyna` (nazwa,logo,trener) VALUES ('Kaczki','kaczka.png','trener@wp.pl');
INSERT INTO `Druzyna` (nazwa,logo,trener) VALUES ('Gęsi','kaczka.png','trener1@wp.pl');


-- players
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Adam','Adamski','aadamski@wp.pl','5828b4bc','856f52e4f0b9595b86e217fbd16161dc0f637a139d520ff6f5ad5929a1a4196b');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('aadamski@wp.pl','Kaczki',34);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Badam','Badamski','bbadamski@interia.pl','a0f01e10','7f44c2844ddec0028da5f43af1f931934b6a882423589981f8031cb26ab35dda');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('bbadamski@interia.pl','Kaczki',12);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Bocian','Bocilawski','bocian@wp.pl','5828b4bc','856f52e4f0b9595b86e217fbd16161dc0f637a139d520ff6f5ad5929a1a4196b');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('bocian@wp.pl','Kaczki',51);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Zbyszek','Bogdanzki','zbychu@interia.pl','a0f01e10','7f44c2844ddec0028da5f43af1f931934b6a882423589981f8031cb26ab35dda');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('zbychu@interia.pl','Kaczki',23);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Adam','Adamski','aadamski2@wp.pl','5828b4bc','856f52e4f0b9595b86e217fbd16161dc0f637a139d520ff6f5ad5929a1a4196b');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('aadamski2@wp.pl','Gęsi',63);
INSERT INTO `Osoba` (imie,nazwisko,email,salt,password) VALUES ('Eustaychy','Badamski','euchy@interia.pl','a0f01e10','7f44c2844ddec0028da5f43af1f931934b6a882423589981f8031cb26ab35dda');
INSERT INTO `Zawodnik` (email,druzyna,numer) VALUES ('euchy@interia.pl','Gęsi',99);

-- team
INSERT INTO `Sklad` (id,trener) VALUES (1,'trener@wp.pl');
INSERT INTO `Sklad` (id,trener) VALUES (2,'trener@wp.pl');

-- teamPlayer
INSERT INTO `TworzySklad` (skladId,zawodnikEmail,rezerwa) VALUES (1,'bbadamski@interia.pl',0);
INSERT INTO `TworzySklad` (skladId,zawodnikEmail,rezerwa) VALUES (1,'aadamski@wp.pl',1);

-- form
INSERT INTO `Wniosek` (id,data,status,uwagi,rozpatrujacy,zglaszajacy) VALUES (1,'2019-01-27 22:01:05.521000',0,NULL,NULL,'trener@wp.pl');
INSERT INTO `WniosekSkladowy` (WniosekId, sklad) VALUES (1, 1);

INSERT INTO `Wniosek` (id,data,status,uwagi,rozpatrujacy,zglaszajacy) VALUES (2,'2019-01-27 22:01:05.521000',0,NULL,NULL,'trener@wp.pl');
INSERT INTO `wniosekDruzynowy` (WniosekId) VALUES (2);
INSERT INTO `Wniosek` (id,data,status,uwagi,rozpatrujacy,zglaszajacy) VALUES (3,'2019-01-27 22:01:05.521000',0,NULL,NULL,'trener1@wp.pl');
INSERT INTO `wniosekDruzynowy` (WniosekId) VALUES (3);

COMMIT;
