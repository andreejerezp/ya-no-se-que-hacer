# DECISIONES_PENDIENTES.md
**Proyecto:** TDFI103 - Bases de Datos (Fase 2: Implementación de Base de Datos y Producto Mínimo Viable asistido por IA)[cite: 1]  
**Caso:** Caso 1 - Sistema Integral de Gestión de Parques Naturales y Conservación Ambiental[cite: 1]  
**Grupo:** Grupo 1 (Agustín Medina Zuñiga, Agustín Jerez Prado, Cristóbal Pastrian Garrido)[cite: 10]  

---

## 1. Resolución de reglas de administración y compartición territorial de parques
* **Descripción:** Definir cómo conviven la administración de un parque por parte de una comunidad autónoma, la compartición territorial entre varias comunidades autónomas y la relación `1:1` `"Administra"` entre trabajador y parque natural que aparece en el modelo relacional de Fase 1[cite: 11, 13, 14].
* **Documento y sección de origen:**
  * *Informe Fase 1*, Sección 2 (Reglas de negocio 1 y 2)[cite: 11], Sección 3 (MERE)[cite: 13] y Sección 4 (Transformación al modelo relacional: `PARQUE_NATURAL` y `COMPARTEN`)[cite: 14, 15].
  * *Enunciado Fase 2*, Sección 5 (Corrección del MERE y construcción del modelo relacional)[cite: 3] y Sección 13 (Punto 3: Correcciones a las reglas de negocio de la fase 1)[cite: 8].
* **Alternativas posibles:**
  * Mantener ambas relaciones (`Administra` con comunidad y `Comparten` M:N con porcentaje territorial) y documentar explícitamente la regla de negocio del trabajador que administra el parque (`idTrabajador` en `PARQUE_NATURAL`)[cite: 11, 14].
  * Depurar o unificar la administración institucional del parque en las reglas de negocio para eliminar contradicciones entre el MERE, las reglas escritas y el modelo relacional[cite: 3, 8, 11].
* **Impacto en el modelo o la aplicación:** Define las claves foráneas de `PARQUE_NATURAL`, la estructura de la tabla asociativa `COMPARTEN` y el poblamiento coherente de comunidades administradoras (5 a 10) y parques (12 a 20)[cite: 4, 14, 15].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: Revisión y corrección del MERE / Modelo relacional final)[cite: 8].
* **Estado:** Pendiente

---

## 2. Modelamiento de roles, funciones del personal y cuentas de usuario del PMV
* **Descripción:** Definir cómo se articulan los roles/funciones del personal (para responder el requerimiento R8 sobre trabajadores que desempeñan más de una función y en qué parques o áreas desarrollan sus actividades) con las cuentas de usuario/roles con permisos diferenciados exigidas para el inicio de sesión del PMV[cite: 4, 5, 6].
* **Documento y sección de origen:**
  * *Informe Fase 1*, Sección 3 (MERE: entidad `Rol`, relación `desempeña` y atributo multivaluado `funciones`)[cite: 13] y Sección 4 (`TRABAJADOR`, `TRABAJADOR_FUNCIONES`, `ROL`)[cite: 14].
  * *Enunciado Fase 2*, Sección 6 (Poblamiento: Usuarios / roles 40 a 80 asociados al personal)[cite: 4], Sección 7 (Requerimiento R8)[cite: 5] y Sección 10 (Funcionalidad 3: Control de usuarios)[cite: 6].
* **Alternativas posibles:**
  * Separar las funciones operativas del personal (`TRABAJADOR_FUNCIONES` / asignación a parque o área para R8) de las credenciales y roles de acceso al sistema PMV asociados al personal[cite: 4, 5, 6, 14].
  * Integrar atributos o entidades de acceso al sistema vinculadas a `TRABAJADOR` que soporten tanto la consulta R8 como la autenticación con al menos 2 roles diferenciados[cite: 4, 5, 6].
* **Impacto en el modelo o la aplicación:** Afecta directamente las tablas de personal, funciones, asignaciones territoriales (parque/área), autenticación en Streamlit y la vista correspondiente a R8[cite: 4, 5, 6, 14].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapas: Revisión y corrección del MERE / Usuarios y roles)[cite: 8].
* **Estado:** Pendiente

---

## 3. Estructura de claves e integridad en inscripciones, asistencia y evaluaciones
* **Descripción:** Confirmar la estructura final de `INSCRIPCION` y `EVALUACION` (en Fase 1 `EVALUACION` tiene `idInscripcion` como PK/FK y `numCorrelativoEval` como atributo simple) y los tipos/restricciones para `asistencia`, `capacidad` y `calificacion`[cite: 16].
* **Documento y sección de origen:**
  * *Informe Fase 1*, Sección 2 (Reglas 6, 7 y 8)[cite: 12] y Sección 4 (`EXCURSION`, `INSCRIPCION`, `EVALUACION`)[cite: 16].
  * *Enunciado Fase 2*, Sección 5 (Restricciones PK, FK, NOT NULL, UNIQUE, CHECK)[cite: 3], Sección 7 (Requerimientos R1, R3, R4, R5, R9, R11, R12)[cite: 5] y Sección 10 (Formulario transaccional)[cite: 6].
* **Alternativas posibles:**
  * Mantener `idInscripcion` como PK/FK en `EVALUACION` (garantizando relación `1:1` estricta por inscripción válida según Regla 6) con restricciones `CHECK` en calificación y asistencia[cite: 3, 12, 16].
  * Usar un identificador propio para `EVALUACION` manteniendo `UNIQUE` sobre `idInscripcion` para preservar la regla de una sola evaluación por inscripción[cite: 3, 12].
* **Impacto en el modelo o la aplicación:** Condiciona las restricciones DDL (`CHECK`, `UNIQUE`, `NOT NULL`), la validación de cupos en el formulario transaccional y los cálculos de tasa de asistencia (R5) y promedios de evaluación (R3, R11)[cite: 3, 5, 6].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapas: Modelo relacional final / Implementación DDL)[cite: 8].
* **Estado:** Pendiente

---

## 4. Selección y flujo de la operación del Formulario Transaccional del PMV
* **Descripción:** Definir la operación transaccional exacta que implementará el PMV, sus validaciones de campos y capacidad, y cómo registrará el estado de asistencia respetando las claves foráneas[cite: 6].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 10 (Tabla de funcionalidades PMV, punto 1: Formulario transaccional)[cite: 6].
  * *Rúbrica Fase 2*, Criterio 4 (Cumplimiento funcional del PMV)[cite: 19].
* **Alternativas posibles:**
  * Registrar una inscripción de un visitante existente a una excursión existente, validando disponibilidad de cupos respecto a `capacidad`, registrando el estado de `asistencia` y respetando las FK[cite: 6, 16].
  * Implementar otra transacción equivalente debidamente justificada sobre el modelo definitivo que cumpla con selección de datos existentes, validación de campos/capacidad e integridad referencial[cite: 6].
* **Impacto en el modelo o la aplicación:** Define los métodos transaccionales en la capa DAO, las consultas parametrizadas de inserción/validación y la interfaz del formulario en Streamlit[cite: 6, 20].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: Formulario transaccional PMV)[cite: 8].
* **Estado:** Pendiente

---

## 5. Selección de tablas maestras/básicas y política de eliminación/desactivación del CRUD
* **Descripción:** Elegir las tablas maestras o básicas (mínimo 2) que tendrán operaciones de creación, consulta, modificación y eliminación o desactivación en el PMV, definiendo cuándo aplicar desactivación lógica frente a eliminación física[cite: 6].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 10 (Tabla de funcionalidades PMV, punto 2: CRUD de tablas básicas)[cite: 6].
  * *Rúbrica Fase 2*, Criterio 4 (Cumplimiento funcional del PMV)[cite: 19].
* **Alternativas posibles:**
  * Implementar CRUD sobre `PARQUE_NATURAL` y `ESPECIE` (citadas como ejemplo en el enunciado)[cite: 6].
  * Seleccionar otras tablas maestras/básicas del modelo definitivo (por ejemplo, `VISITANTE`, `COMUNIDAD_AUTONOMA`, etc.) incorporando un atributo de estado lógico en el modelo relacional si se requiere desactivación por integridad referencial[cite: 3, 6].
* **Impacto en el modelo o la aplicación:** Puede requerir agregar columnas de estado (activo/inactivo) en el modelo relacional y DDL para soportar desactivación lógica sin violar FK[cite: 3, 6].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: CRUD PMV)[cite: 8].
* **Estado:** Pendiente

---

## 6. Definición de roles y matriz de permisos del Control de Usuarios del PMV
* **Descripción:** Establecer los roles (mínimo 2) disponibles para el inicio de sesión en el PMV y los permisos diferenciados que restringirán el acceso real a funcionalidades de la aplicación[cite: 6].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 6 (Usuarios / roles: cuentas asociadas al personal con al menos dos roles y permisos diferenciados)[cite: 4] y Sección 10 (Funcionalidad 3: Control de usuarios)[cite: 6].
  * *Rúbrica Fase 2*, Criterio 4 (Cumplimiento funcional del PMV)[cite: 19].
* **Alternativas posibles:**
  * Definir un rol con acceso completo (gestión de CRUD, formulario transaccional y dashboard) y otro rol con acceso restringido (por ejemplo, solo consulta/dashboard o registro operativo limitado), coherentes con los roles del personal en la BD[cite: 4, 6].
* **Impacto en el modelo o la aplicación:** Determina los registros de usuarios/roles en el script de poblamiento, el manejo de sesión en Streamlit y el control de acceso en vistas/módulos del PMV[cite: 4, 6, 20].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: Usuarios y roles)[cite: 8].
* **Estado:** Pendiente

---

## 7. Formulación y justificación de la cuarta pregunta de negocio del Dashboard
* **Descripción:** Definir la cuarta pregunta de negocio del dashboard en Streamlit, asegurando que sea relevante, no equivalente a las tres preguntas de Fase 1, resoluble mediante consulta SQL y acompañada de una visualización adecuada y justificación de decisión de negocio[cite: 7].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 2 (Resultado esperado)[cite: 2], Sección 10 (Funcionalidad 4: Panel de información / dashboard)[cite: 6] y Sección 10.1 (Dashboard: Pregunta 4 propuesta por el equipo)[cite: 7].
  * *Rúbrica Fase 2*, Criterio 4 (Cumplimiento funcional del PMV)[cite: 19].
* **Alternativas posibles:**
  * Formular una pregunta orientada a conservación ambiental, proyectos científicos, inventarios por área o desempeño/asistencia de excursiones que utilice tablas del modelo definitivo sin duplicar las 3 preguntas de Fase 1[cite: 7].
* **Impacto en el modelo o la aplicación:** Requiere diseñar una consulta SQL específica en el PMV, generar su visualización en Plotly e incluir su justificación de negocio en el informe y presentación[cite: 2, 7].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: Dashboard)[cite: 8].
* **Estado:** Pendiente

---

## 8. Estrategia de poblamiento sintético y volúmenes exactos por tabla
* **Descripción:** Determinar los volúmenes exactos de registros por entidad (dentro de los rangos orientativos del enunciado) y las reglas de distribución (fechas, estados de asistencia, tipos de especies clasificadas y sin clasificar, calificaciones) para garantizar resultados no triviales en R1–R12 y el dashboard[cite: 4].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 3 (Faker para Python)[cite: 2], Sección 6 (Poblamiento de la base de datos)[cite: 4] y Sección 8 (Script integral de implementación)[cite: 6].
  * *Rúbrica Fase 2*, Criterio 2 (Construcción y población de la base de datos)[cite: 19].
* **Alternativas posibles:**
  * Generar los datos mediante script en Python con Faker reproduciendo inserciones SQL consolidadas en el script integral y en el script de generación de datos, usando semilla fija para reproducibilidad[cite: 1, 2, 4, 6].
* **Impacto en el modelo o la aplicación:** Asegura que ninguna vista (R2, R3, R5, R6, R7, R8), procedimiento almacenado (R1, R4, R9, R10, R11, R12) ni gráfico del dashboard devuelva conjuntos vacíos o triviales[cite: 4, 5, 7].
* **Responsable por definir:** Por asignar en la Matriz de Responsabilidades (Etapa: Poblamiento y calidad de datos)[cite: 8].
* **Estado:** Pendiente

---

## 9. Distribución de responsabilidades en la Matriz del Equipo
* **Descripción:** Asignar responsables principales y colaboradores para las 15 actividades de la matriz de Fase 2, cumpliendo las restricciones de equilibrio, participación en más de una etapa por integrante y responsables principales distintos para cada una de las 4 funcionalidades del PMV[cite: 8, 9].
* **Documento y sección de origen:**
  * *Enunciado Fase 2*, Sección 14 (Plan de responsabilidades y participación del equipo)[cite: 8, 9] y Sección 15 (Bitácora individual de trabajo)[cite: 9].
  * *Rúbrica Fase 2*, Criterio 7 (Gestión, matriz de responsabilidades y coherencia de bitácoras)[cite: 20].
* **Alternativas posibles:**
  * Distribuir las 15 etapas entre los 3 integrantes del Grupo 1 (Agustín Medina, Agustín Jerez y Cristóbal Pastrian) asegurando que los 4 módulos del PMV (Formulario transaccional, CRUD, Usuarios/roles y Dashboard) queden liderados por distintos integrantes y que el cuarto módulo sea liderado por quien tenga menor carga en otras etapas[cite: 8, 9, 10].
* **Impacto en el modelo o la aplicación:** Define la trazabilidad entre la matriz, las bitácoras individuales, el desarrollo real del código y la preparación para la defensa individual[cite: 8, 9, 20, 21].
* **Responsable por definir:** Todos los integrantes del Grupo 1 (antes de iniciar la implementación)[cite: 8, 10].
* **Estado:** Pendiente