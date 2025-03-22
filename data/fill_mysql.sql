-- Fahrzeuge
LOAD DATA INFILE '/var/lib/mysql-files/01_fahrzeug.csv'
INTO TABLE Fahrzeug
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, hersteller, modell, baujahr);

-- Fahrer
LOAD DATA INFILE '/var/lib/mysql-files/02_fahrer.csv'
INTO TABLE Fahrer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, vorname, nachname, geburtsdatum, kontakt_nr, email);

-- Fahrer-Fahrzeug
LOAD DATA INFILE '/var/lib/mysql-files/03_fahrer_fahrzeug.csv'
INTO TABLE Fahrer_Fahrzeug
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(fahrerid, fahrzeugid, gueltig_ab, gueltig_bis);

-- Geräte
LOAD DATA INFILE '/var/lib/mysql-files/04_geraet.csv'
INTO TABLE Geraet
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrzeugid, geraet_typ, hersteller, modell);

-- Fahrten
LOAD DATA INFILE '/var/lib/mysql-files/05_fahrt.csv'
INTO TABLE Fahrt
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrzeugid, geraetid, @startzeitpunkt, @endzeitpunkt, route)
SET 
    startzeitpunkt = STR_TO_DATE(@startzeitpunkt, '%d.%m.%Y %H:%i'),
    endzeitpunkt = STR_TO_DATE(@endzeitpunkt, '%d.%m.%Y %H:%i');;

-- Fahrzeugparameter
LOAD DATA INFILE '/var/lib/mysql-files/07_fahrzeugparameter.csv'
INTO TABLE Fahrzeugparameter
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrtid, zeitstempel, geschwindigkeit, motortemperatur, luftmassenstrom, batterie);

-- Beschleunigung
LOAD DATA INFILE '/var/lib/mysql-files/08_beschleunigung.csv'
INTO TABLE Beschleunigung
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrtid, zeitstempel, x_achse, y_achse, z_achse);

-- Diagnose
LOAD DATA INFILE '/var/lib/mysql-files/09_diagnose.csv'
INTO TABLE Diagnose
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrtid, @zeitstempel, fehlercode, beschreibung)
SET 
    zeitstempel = STR_TO_DATE(@zeitstempel, '%Y-%m-%d %H:%i:%s');

-- Wartung
LOAD DATA INFILE '/var/lib/mysql-files/10_wartung.csv'
INTO TABLE Wartung
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, fahrzeugid, datum, beschreibung);

-- Gerät-Installation
LOAD DATA INFILE '/var/lib/mysql-files/11_geraet_installation.csv'
INTO TABLE Geraet_Installation
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, geraetid, fahrzeugid, einbau_datum, ausbau_datum);

-- Fahrer-Fahrt
-- 1. Erstelle eine temporäre Tabelle ohne Foreign Key-Beschränkungen
CREATE TEMPORARY TABLE temp_fahrt_fahrer (
    fahrtid INT,
    fahrerid INT
);

-- 2. Lade die Daten in die temporäre Tabelle
LOAD DATA INFILE '/var/lib/mysql-files/06_fahrt_fahrer.csv'
INTO TABLE temp_fahrt_fahrer
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(fahrtid, fahrerid);

-- 3. Füge nur die gültigen Zeilen (mit existierender fahrtid) in die endgültige Tabelle ein
INSERT INTO Fahrt_Fahrer (fahrtid, fahrerid)
SELECT t.fahrtid, t.fahrerid
FROM temp_fahrt_fahrer t
JOIN Fahrt f ON t.fahrtid = f.id;

-- 4. Lösche die temporäre Tabelle, wenn fertig
DROP TABLE IF EXISTS temp_fahrt_fahrer;