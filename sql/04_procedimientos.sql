-- Caso 1: Parques Naturales | MySQL 8.4
-- 6 procedimientos oficiales: R1, R4, R9, R10, R11 y R12.
USE caso1_parques_naturales;

DROP PROCEDURE IF EXISTS sp_R1_areas_mayor_visitacion_periodo;
DROP PROCEDURE IF EXISTS sp_R4_parques_excursiones_visitantes_periodo;
DROP PROCEDURE IF EXISTS sp_R9_excursiones_sobre_promedio_parque;
DROP PROCEDURE IF EXISTS sp_R10_especies_superiores_promedio_tipo;
DROP PROCEDURE IF EXISTS sp_R11_visitantes_superiores_promedios;
DROP PROCEDURE IF EXISTS sp_R12_parques_promedio_visitantes_excursion;

DELIMITER $$

-- R1: Áreas con mayor cantidad de visitantes mediante excursiones en un período.
CREATE PROCEDURE sp_R1_areas_mayor_visitacion_periodo(
    IN p_fecha_inicio DATE,
    IN p_fecha_termino DATE
)
BEGIN
    SELECT pn.numCorrelativo, pn.nombre AS parque,
           a.numInterno, a.nombre AS area,
           COUNT(i.idInscripcion) AS totalInscripciones,
           COUNT(DISTINCT i.idVisitante) AS visitantesUnicos
    FROM PARQUE_NATURAL pn
    JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
    JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                      AND ex.numInterno = a.numInterno
    LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                            AND i.numInterno = ex.numInterno
                            AND i.codigoExcursion = ex.codigoExcursion
    WHERE ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
    GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre
    ORDER BY visitantesUnicos DESC, totalInscripciones DESC;
END$$


-- R4: Parques con más excursiones y visitantes en un período.
CREATE PROCEDURE sp_R4_parques_excursiones_visitantes_periodo(
    IN p_fecha_inicio DATE,
    IN p_fecha_termino DATE
)
BEGIN
    SELECT pn.numCorrelativo, pn.nombre AS parque,
           COUNT(DISTINCT CONCAT(ex.numCorrelativo, '-', ex.numInterno, '-', ex.codigoExcursion)) AS totalExcursiones,
           COUNT(i.idInscripcion) AS totalInscripciones,
           COUNT(DISTINCT i.idVisitante) AS visitantesUnicos
    FROM PARQUE_NATURAL pn
    LEFT JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
    LEFT JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                           AND ex.numInterno = a.numInterno
                           AND ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
    LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                            AND i.numInterno = ex.numInterno
                            AND i.codigoExcursion = ex.codigoExcursion
    GROUP BY pn.numCorrelativo, pn.nombre
    ORDER BY totalExcursiones DESC, totalInscripciones DESC;
END$$


-- R9: Excursiones que superan el promedio de inscripciones de excursiones del mismo parque/período.
CREATE PROCEDURE sp_R9_excursiones_sobre_promedio_parque(
    IN p_numCorrelativo INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_termino DATE
)
BEGIN
    SELECT pn.numCorrelativo, pn.nombre AS parque,
           a.numInterno, a.nombre AS area,
           ex.codigoExcursion, ex.modalidad, ex.fecha,
           COUNT(i.idInscripcion) AS visitantesInscritos
    FROM PARQUE_NATURAL pn
    JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
    JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                      AND ex.numInterno = a.numInterno
    LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                            AND i.numInterno = ex.numInterno
                            AND i.codigoExcursion = ex.codigoExcursion
    WHERE pn.numCorrelativo = p_numCorrelativo
      AND ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
    GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre,
             ex.codigoExcursion, ex.modalidad, ex.fecha
    HAVING COUNT(i.idInscripcion) > (
        SELECT AVG(resumen.cantidadInscritos)
        FROM (
            SELECT COUNT(i2.idInscripcion) AS cantidadInscritos
            FROM EXCURSION ex2
            JOIN AREA a2 ON a2.numCorrelativo = ex2.numCorrelativo
                        AND a2.numInterno = ex2.numInterno
            LEFT JOIN INSCRIPCION i2 ON i2.numCorrelativo = ex2.numCorrelativo
                                    AND i2.numInterno = ex2.numInterno
                                    AND i2.codigoExcursion = ex2.codigoExcursion
            WHERE a2.numCorrelativo = p_numCorrelativo
              AND ex2.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
            GROUP BY ex2.numCorrelativo, ex2.numInterno, ex2.codigoExcursion
        ) AS resumen
    )
    ORDER BY visitantesInscritos DESC;
END$$


-- R10: Especies cuya cantidad inventariada supera el promedio de especies del mismo tipo.
-- p_tipo acepta 'Vegetal', 'Animal' o 'Mineral'; las especies sin subtipo no se comparan.
CREATE PROCEDURE sp_R10_especies_superiores_promedio_tipo(IN p_tipo VARCHAR(20))
BEGIN
    WITH especies_tipo AS (
        SELECT idEspecie, 'Vegetal' AS tipo FROM VEGETAL
        UNION ALL SELECT idEspecie, 'Animal' AS tipo FROM ANIMAL
        UNION ALL SELECT idEspecie, 'Mineral' AS tipo FROM MINERAL
    ),
    total_especie AS (
        SELECT et.idEspecie, et.tipo, e.nombreVulgar,
               COALESCE(SUM(ie.cantidadInventario), 0) AS cantidadTotal
        FROM especies_tipo et
        JOIN ESPECIE e ON e.idEspecie = et.idEspecie
        LEFT JOIN INVENTARIO_ESPECIE ie ON ie.idEspecie = et.idEspecie
        GROUP BY et.idEspecie, et.tipo, e.nombreVulgar
    )
    SELECT te.idEspecie, te.tipo, te.nombreVulgar, te.cantidadTotal
    FROM total_especie te
    WHERE UPPER(TRIM(te.tipo)) = UPPER(TRIM(p_tipo))
      AND te.cantidadTotal > (
          SELECT AVG(te2.cantidadTotal)
          FROM total_especie te2
          WHERE te2.tipo = te.tipo
      )
    ORDER BY te.cantidadTotal DESC;
END$$


-- R11: Visitantes que superan el promedio de excursiones y promedio global de evaluación.
CREATE PROCEDURE sp_R11_visitantes_superiores_promedios(
    IN p_fecha_inicio DATE,
    IN p_fecha_termino DATE
)
BEGIN
    SELECT resumen_visitante.idVisitante,
           resumen_visitante.visitante,
           resumen_visitante.excursionesParticipadas,
           evaluacion_visitante.promedioEvaluacionVisitante
    FROM (
        SELECT v.idVisitante, v.nombre AS visitante,
               COUNT(DISTINCT CONCAT(i.numCorrelativo, '-', i.numInterno, '-', i.codigoExcursion)) AS excursionesParticipadas
        FROM VISITANTE v
        JOIN INSCRIPCION i ON i.idVisitante = v.idVisitante
        JOIN EXCURSION ex ON ex.numCorrelativo = i.numCorrelativo
                          AND ex.numInterno = i.numInterno
                          AND ex.codigoExcursion = i.codigoExcursion
        WHERE ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
        GROUP BY v.idVisitante, v.nombre
    ) AS resumen_visitante
    JOIN (
        SELECT i.idVisitante, AVG(ev.calificacion) AS promedioEvaluacionVisitante
        FROM INSCRIPCION i
        JOIN EXCURSION ex ON ex.numCorrelativo = i.numCorrelativo
                          AND ex.numInterno = i.numInterno
                          AND ex.codigoExcursion = i.codigoExcursion
        JOIN EVALUACION ev ON ev.idInscripcion = i.idInscripcion
        WHERE ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
        GROUP BY i.idVisitante
    ) AS evaluacion_visitante
      ON evaluacion_visitante.idVisitante = resumen_visitante.idVisitante
    WHERE resumen_visitante.excursionesParticipadas > (
        SELECT AVG(per_visitante.cantidadExcursiones)
        FROM (
            SELECT COUNT(DISTINCT CONCAT(i2.numCorrelativo, '-', i2.numInterno, '-', i2.codigoExcursion)) AS cantidadExcursiones
            FROM INSCRIPCION i2
            JOIN EXCURSION ex2 ON ex2.numCorrelativo = i2.numCorrelativo
                              AND ex2.numInterno = i2.numInterno
                              AND ex2.codigoExcursion = i2.codigoExcursion
            WHERE ex2.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
            GROUP BY i2.idVisitante
        ) AS per_visitante
    )
    AND evaluacion_visitante.promedioEvaluacionVisitante > (
        SELECT AVG(ev2.calificacion)
        FROM EVALUACION ev2
        JOIN INSCRIPCION i3 ON i3.idInscripcion = ev2.idInscripcion
        JOIN EXCURSION ex3 ON ex3.numCorrelativo = i3.numCorrelativo
                           AND ex3.numInterno = i3.numInterno
                           AND ex3.codigoExcursion = i3.codigoExcursion
        WHERE ex3.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
    )
    ORDER BY resumen_visitante.excursionesParticipadas DESC,
             evaluacion_visitante.promedioEvaluacionVisitante DESC;
END$$


-- R12: Parques con promedio de visitantes inscritos por excursión sobre promedio general de parques.
CREATE PROCEDURE sp_R12_parques_promedio_visitantes_excursion(
    IN p_fecha_inicio DATE,
    IN p_fecha_termino DATE
)
BEGIN
    WITH promedio_por_parque AS (
        SELECT pn.numCorrelativo, pn.nombre AS parque,
               COUNT(i.idInscripcion) / NULLIF(COUNT(DISTINCT CONCAT(ex.numCorrelativo, '-', ex.numInterno, '-', ex.codigoExcursion)), 0) AS promedioVisitantesExcursion
        FROM PARQUE_NATURAL pn
        JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
        JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                          AND ex.numInterno = a.numInterno
                          AND ex.fecha BETWEEN p_fecha_inicio AND p_fecha_termino
        LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                                AND i.numInterno = ex.numInterno
                                AND i.codigoExcursion = ex.codigoExcursion
        GROUP BY pn.numCorrelativo, pn.nombre
    )
    SELECT pp.numCorrelativo, pp.parque, pp.promedioVisitantesExcursion
    FROM promedio_por_parque pp
    WHERE pp.promedioVisitantesExcursion > (
        SELECT AVG(pp2.promedioVisitantesExcursion)
        FROM promedio_por_parque pp2
    )
    ORDER BY pp.promedioVisitantesExcursion DESC;
END$$


DELIMITER ;
