DELIMITER //

CREATE TRIGGER after_fahrzeug_update
AFTER UPDATE ON Fahrzeug
FOR EACH ROW
BEGIN
    IF OLD.hersteller <> NEW.hersteller THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeug', 'hersteller', OLD.hersteller, NEW.hersteller);
    END IF;

    IF OLD.modell <> NEW.modell THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeug', 'modell', OLD.modell, NEW.modell);
    END IF;

    IF OLD.baujahr <> NEW.baujahr THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeug', 'baujahr', OLD.baujahr, NEW.baujahr);
    END IF;
END;
//

CREATE TRIGGER after_fahrer_update
AFTER UPDATE ON Fahrer
FOR EACH ROW
BEGIN
    IF OLD.vorname <> NEW.vorname THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrer', 'vorname', OLD.vorname, NEW.vorname);
    END IF;

    IF OLD.nachname <> NEW.nachname THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrer', 'nachname', OLD.nachname, NEW.nachname);
    END IF;

    IF OLD.geburtsdatum <> NEW.geburtsdatum THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrer', 'geburtsdatum', OLD.geburtsdatum, NEW.geburtsdatum);
    END IF;

    IF OLD.kontakt_nr <> NEW.kontakt_nr THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrer', 'kontakt_nr', OLD.kontakt_nr, NEW.kontakt_nr);
    END IF;

    IF OLD.email <> NEW.email THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrer', 'email', OLD.email, NEW.email);
    END IF;
END;
//

CREATE TRIGGER after_fahrer_fahrzeug_update
AFTER UPDATE ON Fahrer_Fahrzeug
FOR EACH ROW
BEGIN
    IF OLD.fahrerid <> NEW.fahrerid THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrerid, OLD.fahrzeugid, 'Fahrer_Fahrzeug', 'fahrerid', OLD.fahrerid, NEW.fahrerid);
    END IF;

    IF OLD.fahrzeugid <> NEW.fahrzeugid THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrerid, OLD.fahrzeugid, 'Fahrer_Fahrzeug', 'fahrzeugid', OLD.fahrzeugid, NEW.fahrzeugid);
    END IF;

    IF OLD.gueltig_ab <> NEW.gueltig_ab THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrerid, OLD.fahrzeugid, 'Fahrer_Fahrzeug', 'gueltig_ab', OLD.gueltig_ab, NEW.gueltig_ab);
    END IF;

    IF OLD.gueltig_bis <> NEW.gueltig_bis THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrerid, OLD.fahrzeugid, 'Fahrer_Fahrzeug', 'gueltig_bis', OLD.gueltig_bis, NEW.gueltig_bis);
    END IF;
END;
//

CREATE TRIGGER after_geraet_update
AFTER UPDATE ON Geraet
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid <> NEW.fahrzeugid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet', 'fahrzeugid', OLD.fahrzeugid, NEW.fahrzeugid);
    END IF;

    IF OLD.geraet_typ <> NEW.geraet_typ THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet', 'geraet_typ', OLD.geraet_typ, NEW.geraet_typ);
    END IF;

    IF OLD.hersteller <> NEW.hersteller THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet', 'hersteller', OLD.hersteller, NEW.hersteller);
    END IF;

    IF OLD.modell <> NEW.modell THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet', 'modell', OLD.modell, NEW.modell);
    END IF;

END;
//

CREATE TRIGGER after_fahrt_update
AFTER UPDATE ON Fahrt
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid <> NEW.fahrzeugid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrt', 'fahrzeugid', OLD.fahrzeugid, NEW.fahrzeugid);
    END IF;

    IF OLD.geraetid <> NEW.geraetid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrt', 'geraetid', OLD.geraetid, NEW.geraetid);
    END IF;

    IF OLD.startzeitpunkt <> NEW.startzeitpunkt THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrt', 'startzeitpunkt', OLD.startzeitpunkt, NEW.startzeitpunkt);
    END IF;

    IF OLD.endzeitpunkt <> NEW.endzeitpunkt THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrt', 'endzeitpunkt', OLD.endzeitpunkt, NEW.endzeitpunkt);
    END IF;

    IF OLD.route <> NEW.route THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrt', 'route', OLD.route, NEW.route);
    END IF;

END;
//

CREATE TRIGGER after_fahrt_fahrer_update
AFTER UPDATE ON Fahrt_Fahrer
FOR EACH ROW
BEGIN
    IF OLD.fahrtid <> NEW.fahrtid THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrtid, OLD.fahrerid, 'Fahrt_Fahrer', 'fahrtid', OLD.fahrtid, NEW.fahrtid);
    END IF;

    IF OLD.fahrerid <> NEW.fahrerid THEN
        INSERT INTO change_log (id_in_table, secondary_id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.fahrtid, OLD.fahrerid, 'Fahrt_Fahrer', 'fahrerid', OLD.fahrerid, NEW.fahrerid);
    END IF;

END;
//

CREATE TRIGGER after_fahrzeugparameter_update
AFTER UPDATE ON Fahrzeugparameter
FOR EACH ROW
BEGIN
    IF OLD.fahrtid <> NEW.fahrtid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'fahrtid', OLD.fahrtid, NEW.fahrtid);
    END IF;

    IF OLD.zeitstempel <> NEW.zeitstempel THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'zeitstempel', OLD.zeitstempel, NEW.zeitstempel);
    END IF;

    IF OLD.geschwindigkeit <> NEW.geschwindigkeit THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'geschwindigkeit', OLD.geschwindigkeit, NEW.geschwindigkeit);
    END IF;

    IF OLD.motortemperatur <> NEW.motortemperatur THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'motortemperatur', OLD.motortemperatur, NEW.motortemperatur);
    END IF;

    IF OLD.luftmassenstrom <> NEW.luftmassenstrom THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'luftmassenstrom', OLD.luftmassenstrom, NEW.luftmassenstrom);
    END IF;

    IF OLD.batterie <> NEW.batterie THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Fahrzeugparameter', 'batterie', OLD.batterie, NEW.batterie);
    END IF;

END;
//

CREATE TRIGGER after_beschleunigung_update
AFTER UPDATE ON Beschleunigung
FOR EACH ROW
BEGIN
    IF OLD.fahrtid <> NEW.fahrtid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Beschleunigung', 'fahrtid', OLD.fahrtid, NEW.fahrtid);
    END IF;

    IF OLD.zeitstempel <> NEW.zeitstempel THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Beschleunigung', 'zeitstempel', OLD.zeitstempel, NEW.zeitstempel);
    END IF;

    IF OLD.x_achse <> NEW.x_achse THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Beschleunigung', 'x_achse', OLD.x_achse, NEW.x_achse);
    END IF;

    IF OLD.y_achse <> NEW.y_achse THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Beschleunigung', 'y_achse', OLD.y_achse, NEW.y_achse);
    END IF;

    IF OLD.z_achse <> NEW.z_achse THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Beschleunigung', 'z_achse', OLD.z_achse, NEW.z_achse);
    END IF;

END;
//

CREATE TRIGGER after_diagnose_update
AFTER UPDATE ON Diagnose
FOR EACH ROW
BEGIN
    IF OLD.fahrtid <> NEW.fahrtid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Diagnose', 'fahrtid', OLD.fahrtid, NEW.fahrtid);
    END IF;

    IF OLD.zeitstempel <> NEW.zeitstempel THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Diagnose', 'zeitstempel', OLD.zeitstempel, NEW.zeitstempel);
    END IF;

    IF OLD.fehlercode <> NEW.fehlercode THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Diagnose', 'fehlercode', OLD.fehlercode, NEW.fehlercode);
    END IF;

    IF OLD.beschreibung <> NEW.beschreibung THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Diagnose', 'beschreibung', OLD.beschreibung, NEW.beschreibung);
    END IF;

END;
//

CREATE TRIGGER after_wartung_update
AFTER UPDATE ON Wartung
FOR EACH ROW
BEGIN
    IF OLD.fahrzeugid <> NEW.fahrzeugid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Wartung', 'fahrzeugid', OLD.fahrzeugid, NEW.fahrzeugid);
    END IF;

    IF OLD.datum <> NEW.datum THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Wartung', 'datum', OLD.datum, NEW.datum);
    END IF;

    IF OLD.beschreibung <> NEW.beschreibung THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Wartung', 'beschreibung', OLD.beschreibung, NEW.beschreibung);
    END IF;

END;
//

CREATE TRIGGER after_geraet_installation_update
AFTER UPDATE ON Geraet_Installation
FOR EACH ROW
BEGIN
    IF OLD.geraetid <> NEW.geraetid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet_Installation', 'geraetid', OLD.geraetid, NEW.geraetid);
    END IF;

    IF OLD.fahrzeugid <> NEW.fahrzeugid THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet_Installation', 'fahrzeugid', OLD.fahrzeugid, NEW.fahrzeugid);
    END IF;

    IF OLD.einbau_datum <> NEW.einbau_datum THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet_Installation', 'einbau_datum', OLD.einbau_datum, NEW.einbau_datum);
    END IF;

    IF OLD.ausbau_datum <> NEW.ausbau_datum THEN
        INSERT INTO change_log (id_in_table, table_name, column_name, old_value, new_value)
        VALUES (OLD.id, 'Geraet_Installation', 'ausbau_datum', OLD.ausbau_datum, NEW.ausbau_datum);
    END IF;

END;
//

DELIMITER ;
