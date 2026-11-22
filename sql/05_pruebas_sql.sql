-- Pruebas de los 12 requerimientos | Caso 1 | MySQL 8.4
USE caso1_ParquesNaturales;

-- R2 (VIEW): distribución de especies por parque/área/tipo.
SELECT * FROM vw_R2_distribucion_especies_inventariadas
ORDER BY parque, area, tipoEspecie;

-- R3 (VIEW): inscritos y promedio de evaluación por excursión.
SELECT * FROM vw_R3_visitantes_y_evaluacion_excursion
ORDER BY fecha, parque, area;

-- R5 (VIEW): porcentaje de asistencia por área.
SELECT * FROM vw_R5_tasa_asistencia_por_area
ORDER BY tasaAsistenciaPct DESC;

-- R6 (VIEW): especies con inventario por parque/área.
SELECT * FROM vw_R6_inventario_por_especie_parque_area
ORDER BY cantidadTotalInventariada DESC;

-- R7 (VIEW): proyectos con al menos 2 participantes y 2 especies investigadas.
SELECT * FROM vw_R7_proyectos_participacion_cientifica
ORDER BY investigadoresParticipantes DESC, especiesEstudiadas DESC;

-- R8 (VIEW): trabajadores con más de una función y parque asignado.
SELECT * FROM vw_R8_trabajadores_multifuncion
ORDER BY cantidadFunciones DESC, parque;

-- R1 (PROCEDURE): áreas con más visitantes en período. Dataset usa fechas entre 2021 y 2026.
CALL sp_R1_areas_mayor_visitacion_periodo('2021-01-01', '2026-12-31');

-- R4 (PROCEDURE): parques con excursiones y visitantes en período.
CALL sp_R4_parques_excursiones_visitantes_periodo('2021-01-01', '2026-12-31');

-- R9 (PROCEDURE): excursiones que superan promedio de su parque; parque 1 como ejemplo.
CALL sp_R9_excursiones_sobre_promedio_parque(1, '2021-01-01', '2026-12-31');

-- R10 (PROCEDURE): inventario por encima del promedio del tipo Animal.
CALL sp_R10_especies_superiores_promedio_tipo('Animal');
-- También probar los otros tipos:
CALL sp_R10_especies_superiores_promedio_tipo('Vegetal');
CALL sp_R10_especies_superiores_promedio_tipo('Mineral');

-- R11 (PROCEDURE): visitantes que superan los promedios de excursiones y evaluación.
CALL sp_R11_visitantes_superiores_promedios('2021-01-01', '2026-12-31');

-- R12 (PROCEDURE): parques con promedio de visitantes/excursión sobre promedio general.
CALL sp_R12_parques_promedio_visitantes_excursion('2021-01-01', '2026-12-31');
