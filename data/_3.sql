DELIMITER //

CREATE PROCEDURE addFahrt(
    IN p_fahrzeugid INT,
    IN p_geraetid INT,
    IN p_startzeitpunkt DATETIME,
    IN p_endzeitpunkt DATETIME,
    IN p_route VARCHAR(50)
)
BEGIN
    DECLARE v_err_msg VARCHAR(255);
    DECLARE v_new_id INT;

    SELECT IFNULL(MAX(id), 0) + 1 INTO v_new_id
    FROM Fahrt;
    
    START TRANSACTION;

    IF p_fahrzeugid IS NULL THEN
        SET v_err_msg = 'Fahrzeug-ID darf nicht NULL sein';
    ELSEIF p_startzeitpunkt IS NULL THEN
        SET v_err_msg = 'Startzeitpunkt darf nicht NULL sein';
    ELSEIF p_endzeitpunkt IS NULL THEN
        SET v_err_msg = 'Endzeitpunkt darf nicht NULL sein';
    ELSEIF p_route IS NULL THEN
        SET v_err_msg = 'Route darf nicht NULL sein';
    ELSEIF NOT EXISTS (
        SELECT 1 FROM Fahrzeug WHERE id = p_fahrzeugid
    ) THEN
        SET v_err_msg = 'Kein Fahrzeug mit dieser ID gefunden';
    ELSEIF p_geraetid IS NOT NULL AND NOT EXISTS (
        SELECT 1 FROM Fahrzeug WHERE id = p_geraetid
    ) THEN
        SET v_err_msg = 'Kein Gerät mit dieser ID gefunden';
    END IF;

    IF v_err_msg IS NOT NULL THEN
        INSERT INTO error_log(err_msg, table_name)
        VALUES (v_err_msg, 'Fahrt');
        ROLLBACK;
    END IF;

    INSERT INTO Fahrt (id, fahrzeugid, geraetid, startzeitpunkt, endzeitpunkt, route)
    VALUES (v_new_id, p_fahrzeugid, p_geraetid, p_startzeitpunkt, p_endzeitpunkt, p_route);

    COMMIT;

END //

DELIMITER ;
