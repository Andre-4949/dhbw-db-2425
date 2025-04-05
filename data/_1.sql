-- Falls Tabellen existieren, zuerst löschen
DROP TABLE IF EXISTS Geraet_Installation;
DROP TABLE IF EXISTS Wartung;
DROP TABLE IF EXISTS Diagnose;
DROP TABLE IF EXISTS Beschleunigung;
DROP TABLE IF EXISTS Fahrzeugparameter;
DROP TABLE IF EXISTS Fahrt_Fahrer;
DROP TABLE IF EXISTS Fahrt;
DROP TABLE IF EXISTS Geraet;
DROP TABLE IF EXISTS Fahrer_Fahrzeug;
DROP TABLE IF EXISTS Fahrer;
DROP TABLE IF EXISTS Fahrzeug;
DROP TABLE IF EXISTS change_log;
DROP TABLE IF EXISTS error_log;


-- Fahrzeuge
CREATE TABLE Fahrzeug (
    id INT PRIMARY KEY,
    hersteller VARCHAR(50) NOT NULL,
    modell VARCHAR(50) NOT NULL,
    baujahr INT NOT NULL
);

-- Fahrer
CREATE TABLE Fahrer (
    id INT PRIMARY KEY,
    vorname VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    geburtsdatum DATE NOT NULL,
    kontakt_nr VARCHAR(20),
    email VARCHAR(100)	
);

-- Fahrer-Fahrzeug Beziehung
CREATE TABLE Fahrer_Fahrzeug (
    fahrerid INT NOT NULL,
    fahrzeugid INT NOT NULL,
    gueltig_ab DATETIME NOT NULL,
    gueltig_bis DATETIME,
    PRIMARY KEY (fahrerid, fahrzeugid),
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(id) ON DELETE RESTRICT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(id) ON DELETE RESTRICT
);

-- Geräte
CREATE TABLE Geraet (
    id INT PRIMARY KEY,
    fahrzeugid INT NOT NULL,
    geraet_typ VARCHAR(50) NOT NULL,
    hersteller VARCHAR(50) NOT NULL,
    modell VARCHAR(50) NOT NULL,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(id) ON DELETE RESTRICT
);

-- Fahrten
CREATE TABLE Fahrt (
    id INT PRIMARY KEY,
    fahrzeugid INT NOT NULL,
    geraetid INT,
    startzeitpunkt DATETIME NOT NULL,
    endzeitpunkt DATETIME NOT NULL,
    route VARCHAR(50) NOT NULL,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(id) ON DELETE RESTRICT,
    FOREIGN KEY (geraetid) REFERENCES Geraet(id) ON DELETE SET NULL
);

-- Fahrer-Fahrt Beziehung
CREATE TABLE Fahrt_Fahrer (
    fahrtid INT NOT NULL,
    fahrerid INT NOT NULL,
    PRIMARY KEY (fahrtid, fahrerid),
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(id) ON DELETE RESTRICT,
    FOREIGN KEY (fahrerid) REFERENCES Fahrer(id) ON DELETE RESTRICT
);

-- Fahrzeugparameter
CREATE TABLE Fahrzeugparameter (
    id INT PRIMARY KEY,
    fahrtid INT NOT NULL,
    zeitstempel DATETIME NOT NULL,
    geschwindigkeit FLOAT NOT NULL,
    motortemperatur FLOAT NOT NULL,
    luftmassenstrom FLOAT NOT NULL,
    batterie FLOAT NOT NULL,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(id) ON DELETE RESTRICT
);

-- Beschleunigungsdaten
CREATE TABLE Beschleunigung (
    id INT PRIMARY KEY,
    fahrtid INT NOT NULL,
    zeitstempel DATETIME NOT NULL,
    x_achse FLOAT NOT NULL,
    y_achse FLOAT NOT NULL,
    z_achse FLOAT NOT NULL,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(id) ON DELETE RESTRICT
);

-- Diagnoseinformationen
CREATE TABLE Diagnose (
    id INT PRIMARY KEY,
    fahrtid INT NOT NULL,
    zeitstempel DATETIME NOT NULL,
    fehlercode VARCHAR(20) NOT NULL,
    beschreibung TEXT,
    FOREIGN KEY (fahrtid) REFERENCES Fahrt(id) ON DELETE RESTRICT
);

-- Wartung
CREATE TABLE Wartung (
    id INT PRIMARY KEY,
    fahrzeugid INT NOT NULL,
    datum DATETIME NOT NULL,
    beschreibung TEXT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(id) ON DELETE RESTRICT
);

-- Gerät-Installation
CREATE TABLE Geraet_Installation (
    id INT PRIMARY KEY,
    geraetid INT NOT NULL,
    fahrzeugid INT NOT NULL,
    einbau_datum DATE NOT NULL,
    ausbau_datum DATE,
    FOREIGN KEY (geraetid) REFERENCES Geraet(id) ON DELETE RESTRICT,
    FOREIGN KEY (fahrzeugid) REFERENCES Fahrzeug(id) ON DELETE RESTRICT
);

CREATE TABLE change_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_in_table INT NOT NULL,
    secondary_id_in_table INT,
    table_name VARCHAR(50) NOT NULL,
    column_name VARCHAR(50) NOT NULL,
    old_value TEXT,
    new_value TEXT,
    changed_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE error_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    err_msg VARCHAR(255) NOT NULL,
    table_name VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);