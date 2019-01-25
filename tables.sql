ALTER TABLE rozgrywka_druzyny DROP CONSTRAINT FKrozgrywka_411014;
ALTER TABLE rozgrywka_druzyny DROP CONSTRAINT FKrozgrywka_298071;
ALTER TABLE Sedzia DROP CONSTRAINT FKSedzia641230;
ALTER TABLE Trener DROP CONSTRAINT FKTrener988113;
ALTER TABLE Zawodnik DROP CONSTRAINT FKZawodnik853986;
ALTER TABLE ZarzadcaLigi DROP CONSTRAINT FKZarzadcaLi7494;
ALTER TABLE Zawodnik DROP CONSTRAINT FKZawodnik396567;
ALTER TABLE Druzyna DROP CONSTRAINT zarządza;
ALTER TABLE Wniosek DROP CONSTRAINT rozpatruje;
ALTER TABLE Zawodnik DROP CONSTRAINT tworzy;
ALTER TABLE WniosekDruzynowy DROP CONSTRAINT FKWniosekDru464768;
ALTER TABLE WniosekSkladowy DROP CONSTRAINT FKWniosekSkl922362;
ALTER TABLE Raport DROP CONSTRAINT "jest o";
ALTER TABLE Raport DROP CONSTRAINT sporządza;
ALTER TABLE WniosekSkladowy DROP CONSTRAINT FKWniosekSkl137331;
ALTER TABLE Sklad DROP CONSTRAINT "zgloszony przez";
ALTER TABLE Wniosek DROP CONSTRAINT zglasza;
ALTER TABLE Gol DROP CONSTRAINT "padl w";
ALTER TABLE Gol DROP CONSTRAINT FKGol711346;
ALTER TABLE Kartka DROP CONSTRAINT wystawia;
ALTER TABLE Kartka DROP CONSTRAINT otrzymuje;
ALTER TABLE Mecz DROP CONSTRAINT sędziuje;
DROP TABLE IF EXISTS Kartka CASCADE;
DROP TABLE IF EXISTS Zawodnik CASCADE;
DROP TABLE IF EXISTS Mecz CASCADE;
DROP TABLE IF EXISTS Osoba CASCADE;
DROP TABLE IF EXISTS Wniosek CASCADE;
DROP TABLE IF EXISTS Gol CASCADE;
DROP TABLE IF EXISTS Raport CASCADE;
DROP TABLE IF EXISTS Sklad CASCADE;
DROP TABLE IF EXISTS Trener CASCADE;
DROP TABLE IF EXISTS rozgrywka_druzyny CASCADE;
DROP TABLE IF EXISTS Druzyna CASCADE;
DROP TABLE IF EXISTS ZarzadcaLigi CASCADE;
DROP TABLE IF EXISTS WniosekSkladowy CASCADE;
DROP TABLE IF EXISTS WniosekDruzynowy CASCADE;
DROP TABLE IF EXISTS Sedzia CASCADE;
CREATE TABLE Kartka (
  id       int4 NOT NULL, 
  kolor    varchar(255) NOT NULL, 
  sedzia   varchar(255) NOT NULL, 
  zawodnik varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Zawodnik (
  email   varchar(255) NOT NULL, 
  druzyna varchar(255) NOT NULL, 
  sklad   int4 NOT NULL, 
  numer   int4 NOT NULL, 
  PRIMARY KEY (email));
CREATE TABLE Mecz (
  id      int4 NOT NULL, 
  stadion varchar(255), 
  sedzia  varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Osoba (
  imie     varchar(255), 
  nazwisko varchar(255), 
  email    varchar(255) NOT NULL, 
  PRIMARY KEY (email));
CREATE TABLE Wniosek (
  id           int4 NOT NULL, 
  data         varchar(255), 
  status       int4, 
  uwagi        varchar(255), 
  rozpatrujacy varchar(255) NOT NULL, 
  zglaszajacy  varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Gol (
  minuta   int4, 
  mecz     int4 NOT NULL, 
  strzelec varchar(255) NOT NULL);
CREATE TABLE Raport (
  id     int4 NOT NULL, 
  mecz   int4 NOT NULL, 
  sedzia varchar(255) NOT NULL, 
  dane   varchar(1024) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Sklad (
  id     int4 NOT NULL, 
  trener varchar(255) NOT NULL, 
  PRIMARY KEY (id));
CREATE TABLE Trener (
  email         varchar(255) NOT NULL, 
  sklad         int4, 
  numerTelefonu varchar(16), 
  PRIMARY KEY (email));
CREATE TABLE rozgrywka_druzyny (
  druzyna varchar(255) NOT NULL, 
  mecz    int4 NOT NULL, 
  PRIMARY KEY (druzyna, 
  mecz));
CREATE TABLE Druzyna (
  nazwa  varchar(255) NOT NULL, 
  logo   varchar(255), 
  trener varchar(255) NOT NULL, 
  PRIMARY KEY (nazwa));
CREATE TABLE ZarzadcaLigi (
  email varchar(255) NOT NULL, 
  PRIMARY KEY (email));
CREATE TABLE WniosekSkladowy (
  Wniosekid int4 NOT NULL, 
  sklad     int4 NOT NULL, 
  PRIMARY KEY (Wniosekid));
CREATE TABLE WniosekDruzynowy (
  Wniosekid int4 NOT NULL, 
  PRIMARY KEY (Wniosekid));
CREATE TABLE Sedzia (
  email varchar(255) NOT NULL, 
  PRIMARY KEY (email));
ALTER TABLE rozgrywka_druzyny ADD CONSTRAINT FKrozgrywka_411014 FOREIGN KEY (druzyna) REFERENCES Druzyna (nazwa);
ALTER TABLE rozgrywka_druzyny ADD CONSTRAINT FKrozgrywka_298071 FOREIGN KEY (mecz) REFERENCES Mecz (id);
ALTER TABLE Sedzia ADD CONSTRAINT FKSedzia641230 FOREIGN KEY (email) REFERENCES Osoba (email);
ALTER TABLE Trener ADD CONSTRAINT FKTrener988113 FOREIGN KEY (email) REFERENCES Osoba (email);
ALTER TABLE Zawodnik ADD CONSTRAINT FKZawodnik853986 FOREIGN KEY (email) REFERENCES Osoba (email);
ALTER TABLE ZarzadcaLigi ADD CONSTRAINT FKZarzadcaLi7494 FOREIGN KEY (email) REFERENCES Osoba (email);
ALTER TABLE Zawodnik ADD CONSTRAINT FKZawodnik396567 FOREIGN KEY (druzyna) REFERENCES Druzyna (nazwa);
ALTER TABLE Druzyna ADD CONSTRAINT zarządza FOREIGN KEY (trener) REFERENCES Trener (email);
ALTER TABLE Wniosek ADD CONSTRAINT rozpatruje FOREIGN KEY (rozpatrujacy) REFERENCES ZarzadcaLigi (email);
ALTER TABLE Zawodnik ADD CONSTRAINT tworzy FOREIGN KEY (sklad) REFERENCES Sklad (id);
ALTER TABLE WniosekDruzynowy ADD CONSTRAINT FKWniosekDru464768 FOREIGN KEY (Wniosekid) REFERENCES Wniosek (id);
ALTER TABLE WniosekSkladowy ADD CONSTRAINT FKWniosekSkl922362 FOREIGN KEY (Wniosekid) REFERENCES Wniosek (id);
ALTER TABLE Raport ADD CONSTRAINT "jest o" FOREIGN KEY (mecz) REFERENCES Mecz (id);
ALTER TABLE Raport ADD CONSTRAINT sporządza FOREIGN KEY (sedzia) REFERENCES Sedzia (email);
ALTER TABLE WniosekSkladowy ADD CONSTRAINT FKWniosekSkl137331 FOREIGN KEY (sklad) REFERENCES Sklad (id);
ALTER TABLE Sklad ADD CONSTRAINT "zgloszony przez" FOREIGN KEY (trener) REFERENCES Trener (email);
ALTER TABLE Wniosek ADD CONSTRAINT zglasza FOREIGN KEY (zglaszajacy) REFERENCES Trener (email);
ALTER TABLE Gol ADD CONSTRAINT "padl w" FOREIGN KEY (mecz) REFERENCES Mecz (id);
ALTER TABLE Gol ADD CONSTRAINT FKGol711346 FOREIGN KEY (strzelec) REFERENCES Zawodnik (email);
ALTER TABLE Kartka ADD CONSTRAINT wystawia FOREIGN KEY (sedzia) REFERENCES Sedzia (email);
ALTER TABLE Kartka ADD CONSTRAINT otrzymuje FOREIGN KEY (zawodnik) REFERENCES Zawodnik (email);
ALTER TABLE Mecz ADD CONSTRAINT sędziuje FOREIGN KEY (sedzia) REFERENCES Sedzia (email);
