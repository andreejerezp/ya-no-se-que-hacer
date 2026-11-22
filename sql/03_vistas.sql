-- Caso 1: Parques Naturales | MySQL 8.4
-- 6 vistas oficiales: R2, R3, R5, R6, R7 y R8.
-- Base de datos/columnas corresponden al DDL caso1_parques_naturales.
USE caso1_ParquesNaturales;

-- R2: Distribución de especies inventariadas (Vegetal/Animal/Mineral) por parque y área.
CREATE OR REPLACE VIEW vw_R2_distribucion_especies_inventariadas AS
SELECT
    pn.numCorrelativo,
    pn.nombre AS parque,
    a.numInterno,
    a.nombre AS area,
    CASE
        WHEN v.idEspecie IS NOT NULL THEN 'Vegetal'
        WHEN an.idEspecie IS NOT NULL THEN 'Animal'
        WHEN m.idEspecie IS NOT NULL THEN 'Mineral'
        ELSE 'Sin subtipo'
    END AS tipoEspecie,
    COUNT(DISTINCT ie.idEspecie) AS especiesInventariadas,
    SUM(ie.cantidadInventario) AS cantidadTotalInventariada
FROM PARQUE_NATURAL pn
JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
JOIN INVENTARIO_ESPECIE ie ON ie.numCorrelativo = a.numCorrelativo
                                  AND ie.numInterno = a.numInterno
JOIN ESPECIE e ON e.idEspecie = ie.idEspecie
LEFT JOIN VEGETAL v ON v.idEspecie = e.idEspecie
LEFT JOIN ANIMAL an ON an.idEspecie = e.idEspecie
LEFT JOIN MINERAL m ON m.idEspecie = e.idEspecie
GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre, tipoEspecie;

-- R3: Cantidad de inscritos/visitantes por excursión y evaluación promedio.
CREATE OR REPLACE VIEW vw_R3_visitantes_y_evaluacion_excursion AS
SELECT
    pn.numCorrelativo,
    pn.nombre AS parque,
    a.numInterno,
    a.nombre AS area,
    ex.codigoExcursion,
    ex.modalidad,
    ex.fecha,
    ex.capacidad,
    COUNT(DISTINCT i.idInscripcion) AS totalInscripciones,
    COUNT(DISTINCT i.idVisitante) AS visitantesUnicos,
    AVG(ev.calificacion) AS promedioEvaluacion,
    COUNT(DISTINCT ev.idInscripcion) AS totalEvaluaciones
FROM PARQUE_NATURAL pn
JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                  AND ex.numInterno = a.numInterno
LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                        AND i.numInterno = ex.numInterno
                        AND i.codigoExcursion = ex.codigoExcursion
LEFT JOIN EVALUACION ev ON ev.idInscripcion = i.idInscripcion
GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre,
         ex.codigoExcursion, ex.modalidad, ex.fecha, ex.capacidad;

-- R5: Tasa de asistencia sobre inscripciones realizadas. 'Asistio' es el valor del DDL.
CREATE OR REPLACE VIEW vw_R5_tasa_asistencia_por_area AS
SELECT
    pn.numCorrelativo,
    pn.nombre AS parque,
    a.numInterno,
    a.nombre AS area,
    COUNT(i.idInscripcion) AS totalInscripciones,
    SUM(CASE WHEN i.asistencia = 'Asistio' THEN 1 ELSE 0 END) AS totalAsistencias,
    ROUND(100.0 * SUM(CASE WHEN i.asistencia = 'Asistio' THEN 1 ELSE 0 END)
          / NULLIF(COUNT(i.idInscripcion), 0), 2) AS tasaAsistenciaPct
FROM PARQUE_NATURAL pn
JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
LEFT JOIN EXCURSION ex ON ex.numCorrelativo = a.numCorrelativo
                      AND ex.numInterno = a.numInterno
LEFT JOIN INSCRIPCION i ON i.numCorrelativo = ex.numCorrelativo
                        AND i.numInterno = ex.numInterno
                        AND i.codigoExcursion = ex.codigoExcursion
GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre;

-- R6: Total inventariado de cada especie por parque y área.
CREATE OR REPLACE VIEW vw_R6_inventario_por_especie_parque_area AS
SELECT
    pn.numCorrelativo,
    pn.nombre AS parque,
    a.numInterno,
    a.nombre AS area,
    e.idEspecie,
    e.nombreVulgar,
    e.denominacionCientifica,
    SUM(ie.cantidadInventario) AS cantidadTotalInventariada,
    COUNT(ie.codigoInventario) AS registrosInventario
FROM PARQUE_NATURAL pn
JOIN AREA a ON a.numCorrelativo = pn.numCorrelativo
JOIN INVENTARIO_ESPECIE ie ON ie.numCorrelativo = a.numCorrelativo
                           AND ie.numInterno = a.numInterno
JOIN ESPECIE e ON e.idEspecie = ie.idEspecie
GROUP BY pn.numCorrelativo, pn.nombre, a.numInterno, a.nombre,
         e.idEspecie, e.nombreVulgar, e.denominacionCientifica;

-- R7: Proyectos con participación de investigadores y especies estudiadas.
-- HAVING exige al menos 2 trabajadores participantes y 2 especies vinculadas.
CREATE OR REPLACE VIEW vw_R7_proyectos_participacion_cientifica AS
SELECT
    p.idProyecto,
    p.nombre AS proyecto,
    pn.numCorrelativo,
    pn.nombre AS parque,
    COUNT(DISTINCT pa.idTrabajador) AS investigadoresParticipantes,
    COUNT(DISTINCT inv.idEspecie) AS especiesEstudiadas
FROM PROYECTO_CIENTIFICO p
JOIN PARQUE_NATURAL pn ON pn.numCorrelativo = p.numCorrelativo
LEFT JOIN PARTICIPA pa ON pa.idProyecto = p.idProyecto
LEFT JOIN INVESTIGA inv ON inv.idProyecto = p.idProyecto
GROUP BY p.idProyecto, p.nombre, pn.numCorrelativo, pn.nombre
HAVING COUNT(DISTINCT pa.idTrabajador) >= 2
   AND COUNT(DISTINCT inv.idEspecie) >= 2;

-- R8: Trabajadores con más de una función y parque donde están asignados.
-- El DDL no contiene una FK directa trabajador-área, por lo que no se inventa esa asignación.
CREATE OR REPLACE VIEW vw_R8_trabajadores_multifuncion AS
SELECT
    t.idTrabajador,
    t.nombre AS trabajador,
    pn.numCorrelativo,
    pn.nombre AS parque,
    COUNT(DISTINCT tf.funcion) AS cantidadFunciones,
    GROUP_CONCAT(DISTINCT tf.funcion ORDER BY tf.funcion SEPARATOR ', ') AS funciones
FROM TRABAJADOR t
JOIN PARQUE_NATURAL pn ON pn.numCorrelativo = t.numCorrelativo
JOIN TRABAJADOR_FUNCIONES tf ON tf.idTrabajador = t.idTrabajador
GROUP BY t.idTrabajador, t.nombre, pn.numCorrelativo, pn.nombre
HAVING COUNT(DISTINCT tf.funcion) > 1;
