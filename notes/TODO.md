## To-Do Liste

## Teil 1 ➡️
- [x] ER-Modell als PDF 🔴
- [x] SQL-Skripte zur Erstellung des DB-Schemas (lauffähig für MySQL) 🔴

## Teil 2 ➡️
- [x] Import aller Daten in das MySQL-Schema, evtl. Datenbereinigung (über SQL/MySQL) 🔴
- [x] Alle Importe innerhalb von Transaktionen 🔴
- [x] Lauffähige App erstellen (Programmrumpf ergänzen) 🔴
- [x] Konvertierung der Tabellen nach MongoDB, einzeln und als embedded Collection (SQL und/oder Python)
- [x] Logging von Konvertierungen soll in eine Log-Tabelle geschrieben werden (als SQL codiert) 🔴
- [x] Report 1: Durchschnittliche Geschwindigkeit und Motortemperatur für alle Fahrten pro Fahrer im März 2024 (als SQL codiert, Datum bzgl. Fahrt) 🔴
- [x] Report 2: Alle Fahrer finden, die innerhalb der letzten 15 Monate eine Fahrt durchgeführt haben (als SQL codiert, evtl. 15 Monate anpassen) 🔴
- [x] Report 3: Die höchste jemals gemessene Geschwindigkeit für jeden Fahrer (als SQL codiert) 🔴
- [x] Hinzufügen der Collection unfall.json in MongoDB 🔴
- [x] Editieren der MySQL-Tabellen soll in eine Changelog-Tabelle getriggert werden (als SQL codiert) 🔴
- [x] Eine Stored Procedure zum Hinzufügen einer neuen Fahrt (als SQL codiert) 🔴
- [x] Änderungen sollen immer persistent in die MySQL-Datenbank geschrieben werden 🔴

Mögliche Skriptgestaltung:
![grafik](https://github.com/user-attachments/assets/91f65873-4036-46ca-bb5a-86627f044b53)

- Wo im Frontend soll man neue Fahrt mit Stored Procedure hinzufügen können?
  - Nein einfach nur mit schicken
- Soll man selbst die fahrt_fahrer.csv zu eine 1-n-Beziehung vereinfachen?
  - man muss nichts vereinfachen
- Soll die embedded collection komplett alles enthalten?
  - er hat ein Beispiel auf moodle hochgeladen
- Reichen für das Logging der Konvertierungen die Success-Logs?
  - ja das reicht aus, so wie es ist

- Musterlösung embed passt nicht bei Gerätinstallation und Gerät csv, es werden Teile in Fahrzeuge verbaut, für die es keine Einträge in der geraet.csv gibt.
  - Teil für fahrzeug id 1 wird bei fahrzeug id 4 verbaut?