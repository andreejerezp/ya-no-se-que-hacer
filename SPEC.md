# SPEC.md — Especificación del Proyecto Fase 2

**Asignatura:** TDFI103 — Bases de Datos  
**Proyecto:** Fase 2 — Implementación de Base de Datos y Producto Mínimo Viable asistido por IA  
**Caso:** Caso 1 — Sistema Integral de Gestión de Parques Naturales y Conservación Ambiental  
**Grupo:** Grupo 1  
**Estado del documento:** Borrador  
**Estado de las decisiones de diseño:** DD-01 a DD-09 pendientes de aprobación

---

## 1. Objetivo y alcance

El objetivo del proyecto es continuar el desarrollo del Caso 1 realizado durante la Fase 1, revisando y corrigiendo el Modelo Entidad-Relación Extendido (MERE) y el modelo relacional, para posteriormente implementar una base de datos en MySQL y construir un Producto Mínimo Viable (PMV) integrado.


El sistema busca gestionar información relacionada con parques naturales, comunidades autónomas, trabajadores, áreas, excursiones, visitantes, especies, inventarios y proyectos científicos.

### Alcance de la Fase 2
- Revisar y corregir el MERE desarrollado en la Fase 1.
- Construir y validar el modelo relacional definitivo.
- Implementar la base de datos en MySQL 8.x.
- Crear un script integral de instalación y reconstrucción de la base de datos.
- Generar datos sintéticos suficientes, coherentes y reproducibles.
- Resolver los 12 requerimientos de información mediante 6 vistas y 6 procedimientos almacenados.
- Desarrollar una aplicación web PMV con cuatro funcionalidades obligatorias.
- Implementar el acceso a la aplicación mediante usuarios y roles diferenciados.
- Desarrollar un dashboard con las preguntas de negocio requeridas.
- Desplegar la solución mediante Docker y Docker Compose.
- Documentar el desarrollo, las pruebas, el uso de IA y la participación del equipo.

### Fuera del alcance actual
En esta etapa de especificación no se desarrollarán todavía scripts SQL ni código Python. Tampoco se considerarán definitivas las modificaciones del modelo que no hayan sido aprobadas por el equipo.

---

## 2. Requisitos obligatorios y origen

| ID | Requisito | Origen |
|---|---|---|
| RF-01 | Revisar y corregir el MERE de Fase 1. | Enunciado Fase 2, secciones 2 y 5 |
| RF-02 | Mantener coherencia entre reglas de negocio, MERE, especializaciones y modelo relacional. | Enunciado Fase 2, sección 5 |
| RF-03 | Implementar el modelo relacional en MySQL Workbench. | Enunciado Fase 2, sección 5 |
| RF-04 | Definir tablas, atributos, tipos de datos, PK, FK y restricciones de integridad. | Enunciado Fase 2, sección 5; Rúbrica, criterio 1 |
| RF-05 | Disponer de un script integral que reconstruya la base de datos desde cero. | Enunciado Fase 2, secciones 2 y 8 |
| RF-06 | Poblar la base de datos con datos sintéticos coherentes y reproducibles. | Enunciado Fase 2, secciones 4 y 6; Rúbrica, criterio 2 |
| RF-07 | Implementar 12 requerimientos SQL mediante 6 vistas y 6 procedimientos almacenados. | Enunciado Fase 2, sección 7; Rúbrica, criterio 3 |
| RF-08 | Desarrollar un formulario transaccional integrado con la base de datos. | Enunciado Fase 2, sección 10 |
| RF-09 | Implementar CRUD sobre al menos dos tablas maestras o básicas. | Enunciado Fase 2, sección 10; Rúbrica, criterio 4 |
| RF-10 | Implementar inicio de sesión y al menos dos roles con permisos diferenciados. | Enunciado Fase 2, secciones 6 y 10 |
| RF-11 | Implementar un dashboard con las tres preguntas de Fase 1 y una cuarta propuesta por el equipo. | Enunciado Fase 2, secciones 2, 10 y 10.1 |
| RF-12 | Utilizar una arquitectura organizada y separar interfaz, lógica y acceso a datos. | Rúbrica, criterio 5 |
| RF-13 | Implementar el despliegue mediante Docker y Docker Compose. | Enunciado Fase 2, sección 12; Rúbrica, criterio 6 |
| RF-14 | Mantener una matriz de responsabilidades y bitácoras individuales. | Enunciado Fase 2, secciones 14 y 15 |
| RF-15 | Elaborar informe final, presentación y defensa individual. | Enunciado Fase 2, sección 13 y 16; Rúbrica |

### Herramientas requeridas
- ERDPlus o herramienta equivalente para modelamiento.
- MySQL 8.x.
- MySQL Workbench.
- Python 3.12 o superior.
- SQLAlchemy.
- PyMySQL.
- Faker.
- Pandas.
- Plotly.
- Streamlit.
- OpenCode.
- Docker.
- Docker Compose.

---

## 3. Actores y casos de uso

### 3.1 Actores
| Actor | Descripción |
|---|---|
| Comunidad autónoma | Participa en la administración y compartición territorial de parques naturales. |
| Trabajador | Personal del sistema que puede desarrollar funciones, trabajar en parques o áreas y participar en proyectos científicos. |
| Supervisor | Trabajador que puede supervisar a otros trabajadores. |
| Investigador | Trabajador que participa en proyectos científicos. |
| Visitante | Persona que realiza inscripciones a excursiones y puede generar evaluaciones. |
| Usuario del PMV | Persona que se autentica en la aplicación y opera según los permisos de su rol. |
| Equipo de desarrollo | Integrantes responsables del diseño, implementación, validación, documentación y presentación. |
| Docente / evaluador | Evalúa los entregables, la presentación y la defensa individual. |

### 3.2 Casos de uso
| ID | Caso de uso | Descripción |
|---|---|---|
| CU-01 | Reconstruir base de datos | Crear la estructura y cargar datos mediante los scripts del proyecto. |
| CU-02 | Consultar requerimientos SQL | Ejecutar las vistas y procedimientos almacenados R1–R12. |
| CU-03 | Iniciar sesión | Autenticar usuarios y restringir funcionalidades según su rol. |
| CU-04 | Registrar operación transaccional | Registrar una operación real utilizando datos existentes y validaciones. |
| CU-05 | Gestionar tablas mediante CRUD | Crear, consultar, modificar y eliminar o desactivar registros de al menos dos tablas. |
| CU-06 | Consultar dashboard | Visualizar indicadores y gráficos asociados a las preguntas de negocio. |
| CU-07 | Desplegar aplicación | Ejecutar la aplicación y base de datos utilizando Docker Compose. |

Los casos de uso CU-03, CU-04, CU-05 y parte de CU-06 dependen de decisiones pendientes del equipo.

---

## 4. Reglas de negocio

Las reglas de negocio siguientes corresponden a la base desarrollada en Fase 1. Algunas requieren revisión antes de ser consideradas definitivas.

### RN-01 — Administración de parques
Una comunidad autónoma administra de cero a muchos parques naturales, mientras que un parque natural es administrado por una comunidad.

**Estado:** Pendiente de revisión, DD-01.

### RN-02 — Compartición territorial
Un parque natural puede ser compartido por varias comunidades autónomas y una comunidad puede compartir varios parques. La relación registra el porcentaje territorial correspondiente a cada comunidad.

**Estado:** Pendiente de revisión, DD-01.

### RN-03 — Supervisión de trabajadores
Un trabajador puede supervisar a cero o muchos trabajadores, mientras que un trabajador puede tener como máximo un supervisor.

### RN-04 — Clasificación de especies
La clasificación de especies es parcial y disjunta. Una especie puede no pertenecer a ningún subtipo o pertenecer únicamente a uno de los siguientes:
- Vegetal.
- Animal.
- Mineral.

### RN-05 — Participación en proyectos científicos
Un trabajador que participa como investigador puede formar parte de cero o muchos proyectos científicos. Un proyecto científico puede contar con uno o muchos investigadores.

### RN-06 — Evaluaciones
Una inscripción genera una única evaluación según la regla de negocio de Fase 1. Cada evaluación debe estar asociada a una inscripción válida.

**Estado:** Pendiente de revisión de claves y restricciones, DD-03.

### RN-07 — Inscripciones
Un visitante puede realizar una o muchas inscripciones a excursiones. Una excursión puede tener cero o muchas inscripciones.

### RN-08 — Comentarios de evaluación
Una evaluación puede contener comentarios, pero estos son opcionales.

### RN-09 — Áreas de parques
Un parque natural se divide en una o más áreas. Cada área pertenece exclusivamente a un parque natural.

### RN-10 — Excursiones en áreas
En un área se pueden realizar cero o muchas excursiones. Cada excursión se realiza en una única área.

### RN-11 — Integridad de datos
Las relaciones entre las entidades deberán estar respaldadas por claves primarias, claves foráneas y restricciones apropiadas. Las restricciones adicionales serán definidas y justificadas en el modelo definitivo.

---

## 5. Entidades, atributos, claves y relaciones

Esta sección representa la base del modelo relacional presentado en Fase 1. No constituye todavía el modelo definitivo de implementación.

### 5.1 Entidades principales
| Entidad | Atributos | PK | FK |
|---|---|---|---|
| ROL | idRol, nombreRol | idRol | — |
| TRABAJADOR | idTrabajador, nombre, direccion, fechaNacimiento, estadoCuenta, idRol, idSupervisor, numCorrelativo | idTrabajador | idRol, idSupervisor, numCorrelativo |
| TRABAJADOR_FUNCIONES | idTrabajador, funciones | idTrabajador + funciones | idTrabajador |
| TRABAJADOR_CONTACTO | idTrabajador, datosContacto | idTrabajador + datosContacto | idTrabajador |
| COMUNIDAD_AUTONOMA | codigoComunidad, nombre, organismoResp, regionAdmin | codigoComunidad | — |
| PARQUE_NATURAL | numCorrelativo, nombre, superficie, fechaDeclaracion, añoDeclaracion, estadoConservacion, presupuesto, idTrabajador | numCorrelativo | idTrabajador |
| COMPARTEN | numCorrelativo, codigoComunidad, porcentajeTerritorial | numCorrelativo + codigoComunidad | numCorrelativo, codigoComunidad |
| PROYECTO_CIENTIFICO | idProyecto, nombre, objetivo, numCorrelativo | idProyecto | numCorrelativo |
| PARTICIPA | idTrabajador, idProyecto | idTrabajador + idProyecto | idTrabajador, idProyecto |
| ESPECIE | idEspecie, estadoConservacion, fechaIncorporacion, nombreVulgar, denominacionCientifica | idEspecie | — |
| VEGETAL | idEspecie, floracion | idEspecie | idEspecie |
| ANIMAL | idEspecie, alimentacion, periodoCelo | idEspecie | idEspecie |
| MINERAL | idEspecie, caracteristicasMineral, rocas, cristales | idEspecie | idEspecie |
| INVESTIGA | idProyecto, idEspecie | idProyecto + idEspecie | idProyecto, idEspecie |
| AREA | numCorrelativo, numInterno, nombre, estadoOperativo, nivelAcceso, extension | numCorrelativo + numInterno | numCorrelativo |
| SE_DESARROLLA_EN | idProyecto, numCorrelativo, numInterno | idProyecto + numCorrelativo + numInterno | idProyecto, numCorrelativo + numInterno |
| INVENTARIO_ESPECIE | codigoInventario, cantidadInventario, fechaUltimoMonitoreo, observaciones, idEspecie, numCorrelativo, numInterno | codigoInventario | idEspecie, numCorrelativo + numInterno |
| EXCURSION | numCorrelativo, numInterno, codigoExcursion, modalidad, horario, fecha, capacidad | numCorrelativo + numInterno + codigoExcursion | numCorrelativo + numInterno |
| VISITANTE | idVisitante, nombre, contacto, fechaNacimiento | idVisitante | — |
| INSCRIPCION | idInscripcion, numCorrelativo, numInterno, codigoExcursion, idVisitante, asistencia, observaciones | idInscripcion | Excursión, visitante |
| EVALUACION | idInscripcion, numCorrelativoEval, fecha, calificacion, comentario | idInscripcion | idInscripcion |

### 5.2 Relaciones principales
| Relación | Cardinalidad / descripción |
|---|---|
| Comunidad – Parque | Administración, pendiente de reconciliar con compartición territorial. |
| Comunidad – Parque (`COMPARTEN`) | N:M, con porcentaje territorial. |
| Trabajador – Trabajador | Relación recursiva de supervisión 1:N. |
| Rol – Trabajador | Relación de desempeño de roles según Fase 1. |
| Trabajador – Funciones | Funciones múltiples de un trabajador. |
| Trabajador – Proyecto | N:M mediante `PARTICIPA`. |
| Proyecto – Especie | N:M mediante `INVESTIGA`. |
| Parque – Área | 1:N, área dependiente de parque y con clave compuesta. |
| Proyecto – Área | N:M mediante `SE_DESARROLLA_EN`. |
| Área – Inventario | Área relacionada con registros de inventario de especies. |
| Especie – Inventario | Una especie puede aparecer en registros de inventario. |
| Especie – Subtipos | Especialización parcial y disjunta: Vegetal, Animal y Mineral. |
| Área – Excursión | 1:N, cada excursión pertenece a un área. |
| Visitante – Excursión | N:M mediante `INSCRIPCION`. |
| Inscripción – Evaluación | Relación 1:1 según regla de Fase 1, pendiente de validación. |
### 5.3 Consideraciones del modelo
- Los atributos derivados, como edad, no se almacenan directamente.
- Las áreas utilizan una clave compuesta asociada al parque.
- Las excursiones utilizan una clave compuesta asociada al área.
- Las relaciones de muchos a muchos se representan mediante entidades asociativas.
- Las especializaciones de especies deben respetar la restricción disjunta y parcial.
- Las claves y restricciones definitivas deben ser validadas por el equipo antes de implementar.

**Esta sección debe actualizarse después de aprobar las decisiones DD-01, DD-02 y DD-03 y validar el MERE final.**

---

## 6. Requerimientos SQL

Los requerimientos de información deberán implementarse utilizando seis vistas y seis procedimientos almacenados.

| ID | Tipo | Requerimiento |
|---|---|---|
| R1 | Procedimiento | Identificar las áreas con mayor cantidad de visitantes mediante excursiones durante un período determinado. Recibe fechas de inicio y término. |
| R2 | Vista | Mostrar la distribución de especies inventariadas entre vegetales, animales y minerales por parque y área. |
| R3 | Vista | Mostrar la relación entre cantidad de visitantes de una excursión y su evaluación promedio. |
| R4 | Procedimiento | Identificar parques con mayor cantidad de excursiones y visitantes durante un período determinado. Recibe fechas. |
| R5 | Vista | Mostrar las áreas con mayor tasa de asistencia respecto a las inscripciones realizadas. |
| R6 | Vista | Mostrar las especies con mayor cantidad inventariada por parque y área. |
| R7 | Vista | Identificar proyectos científicos con mayor participación de investigadores y especies estudiadas. |
| R8 | Vista | Identificar trabajadores que desempeñan más de una función y los parques o áreas donde desarrollan actividades. |
| R9 | Procedimiento | Identificar excursiones que superan el promedio de visitantes de las excursiones del mismo parque. Recibe parque y período. |
| R10 | Procedimiento | Identificar especies con inventario superior al promedio de especies del mismo tipo. Recibe el tipo de especie. |
| R11 | Procedimiento | Identificar visitantes que superan el promedio de excursiones realizadas y tienen una evaluación promedio superior al promedio general. Recibe rango de fechas. |
| R12 | Procedimiento | Identificar parques cuyo promedio de visitantes por excursión supera el promedio general de parques durante un período. Recibe fechas. |
### Condiciones de implementación SQL
- Total: 6 vistas y 6 procedimientos almacenados.
- Los procedimientos deben incorporar parámetros `IN` útiles.
- Se deberán utilizar las estructuras SQL requeridas por cada consulta, incluyendo agrupaciones, subconsultas, funciones de agregación y subconsultas correlacionadas cuando corresponda.
- Cada requerimiento debe ser probado en MySQL Workbench.
- Las evidencias de ejecución y resultados deberán incluirse en el informe.
- Los requerimientos SQL son independientes de las cuatro funcionalidades obligatorias del PMV.

---

## 7. Las cuatro funcionalidades del PMV

El PMV será una aplicación web construida en Python y Streamlit, conectada a la base de datos MySQL del proyecto.
### PMV-01 — Formulario transaccional
Permitir registrar una operación real de la base de datos mediante un formulario que:
- Seleccione datos existentes.
- Valide los campos ingresados.
- Respete las relaciones y claves foráneas.
- Considere capacidad o disponibilidad cuando corresponda.
- Ejecute una transacción real.
- Maneje errores y evite registros inconsistentes.

La operación específica todavía no está confirmada. **Estado: Pendiente DD-04.**
### PMV-02 — CRUD
Implementar las operaciones crear, consultar, modificar y eliminar o desactivar sobre al menos dos tablas maestras o básicas. La selección de tablas y la política de eliminación física o lógica todavía no están confirmadas.

**Estado: Pendiente DD-05.**
### PMV-03 — Control de usuarios
La aplicación debe contar con inicio de sesión, usuarios asociados al personal según el diseño que se defina, al menos dos roles, permisos diferenciados y restricciones de acceso efectivas a las funcionalidades.

La relación entre los roles operativos del personal y los roles de acceso al PMV debe ser definida. **Estado: Pendiente DD-02 y DD-06.**
### PMV-04 — Dashboard
El dashboard deberá responder las tres preguntas de negocio de la Fase 1 y una cuarta pregunta propuesta por el equipo.
#### Pregunta 1
¿Cuáles son las áreas con mayor cantidad de visitantes mediante excursiones durante un período determinado?
- Filtros de fecha.
- Filtro de parque.
- Visualización de áreas.
- Cantidad de visitantes.
#### Pregunta 2
¿Cómo se distribuyen las especies inventariadas entre vegetales, animales y minerales?
- Distribución por tipo de especie.
- Información de parque y área.
- Filtros según los datos disponibles.
#### Pregunta 3
¿Existe relación entre la cantidad de visitantes de una excursión y su evaluación promedio?
- Número de participantes.
- Promedio de evaluación.
- Gráfico de dispersión.
- Tabla de detalle.
#### Pregunta 4
Será definida y justificada por el equipo. Debe ser distinta a las tres preguntas anteriores, resoluble mediante SQL y contar con una visualización adecuada que permita apoyar una decisión de negocio.

**Estado: Pendiente DD-07.**

---

## 8. Arquitectura tecnológica
### 8.1 Stack
| Componente | Tecnología |
|---|---|
| Modelamiento | ERDPlus o equivalente |
| Base de datos | MySQL 8.x |
| Administración y modelado relacional | MySQL Workbench |
| Lenguaje PMV | Python 3.12+ |
| Framework web | Streamlit |
| ORM / conexión | SQLAlchemy |
| Driver MySQL | PyMySQL |
| Generación de datos | Faker |
| Procesamiento | Pandas |
| Visualización | Plotly |
| Asistente de desarrollo | OpenCode |
| Contenedores | Docker |
| Orquestación | Docker Compose |
### 8.2 Organización lógica
La aplicación deberá separar sus responsabilidades:
1. **Presentación:** interfaz, formularios, tablas, filtros, gráficos y navegación.
2. **Lógica de negocio:** validaciones y procesamiento de operaciones.
3. **Acceso a datos:** consultas y operaciones sobre MySQL, mediante DAO o capa equivalente.
4. **Base de datos:** almacenamiento persistente de la información.
### 8.3 Conexión y seguridad
- Utilizar una conexión centralizada.
- Utilizar consultas parametrizadas.
- Manejar errores de conexión y ejecución.
- Gestionar y cerrar recursos.
- Evitar exposición de credenciales.
- Utilizar permisos diferenciados para el acceso al PMV.
### 8.4 Docker
El proyecto deberá contener `Dockerfile` para la aplicación, `docker-compose.yml`, servicio de aplicación, servicio MySQL 8.x, volumen persistente para la base de datos, variables de entorno para configuración, mecanismo de disponibilidad de la base de datos e inicialización mediante scripts del proyecto.
La aplicación deberá poder ejecutarse mediante:

```bash
docker compose up --build
```

---

## 9. Plan de implementación y pruebas
### Etapa 0 — Decisiones y planificación
- Revisar el registro de decisiones DD-01 a DD-09.
- Confirmar las decisiones de diseño.
- Identificar decisiones que requieren aclaración docente.
- Completar la matriz de responsabilidades.
### Etapa 1 — Corrección del MERE
- Revisar el modelo de Fase 1.
- Revisar las reglas de negocio.
- Incorporar las correcciones acordadas.
- Documentar los cambios realizados.
### Etapa 2 — Modelo relacional
- Definir tablas definitivas.
- Definir atributos y tipos.
- Definir PK y FK.
- Definir restricciones de integridad.
- Revisar relaciones y cardinalidades.
- Validar el modelo en MySQL Workbench.
### Etapa 3 — Base de datos y poblamiento
- Implementar la estructura de la base de datos.
- Crear restricciones.
- Generar datos sintéticos.
- Validar relaciones e integridad.
- Confirmar que los datos permiten ejecutar todos los requerimientos.

Los volúmenes definitivos de datos se encuentran pendientes de definición.
### Etapa 4 — Requerimientos SQL
- Implementar R1–R12.
- Crear las seis vistas.
- Crear los seis procedimientos almacenados.
- Ejecutar pruebas.
- Registrar resultados.
- Documentar cada requerimiento.
### Etapa 5 — Desarrollo PMV
Implementar por separado las cuatro funcionalidades: formulario transaccional, CRUD, control de usuarios y dashboard. Luego integrar las funcionalidades en una única aplicación.
### Etapa 6 — Pruebas e integración
- Probar las operaciones de base de datos.
- Probar integridad referencial.
- Probar restricciones.
- Probar el formulario transaccional.
- Probar CRUD.
- Probar roles y permisos.
- Probar visualizaciones.
- Probar la conexión entre la aplicación y MySQL.
### Etapa 7 — Docker y despliegue
- Construir la imagen de la aplicación.
- Configurar los servicios.
- Configurar persistencia.
- Verificar la inicialización.
- Ejecutar `docker compose up --build`.
- Validar el funcionamiento completo.
### Etapa 8 — Documentación y presentación
- Completar el informe.
- Incorporar evidencias de las pruebas.
- Completar las bitácoras individuales.
- Finalizar la matriz de responsabilidades.
- Preparar la presentación.
- Preparar la defensa individual.
### Plan de pruebas
| ID | Prueba | Resultado esperado |
|---|---|---|
| PT-01 | Creación de BD desde cero | La estructura se crea sin errores. |
| PT-02 | Ejecución del poblamiento | Los datos se cargan correctamente. |
| PT-03 | Integridad de FK | No se permiten referencias inexistentes. |
| PT-04 | Restricciones de datos | PK, UNIQUE, CHECK y NOT NULL se comportan correctamente según lo definido. |
| PT-05 | Requerimientos SQL R1–R12 | Las consultas entregan resultados coherentes con los datos de prueba. |
| PT-06 | Formulario transaccional | La operación se registra correctamente o se revierte ante un error. |
| PT-07 | CRUD | Las operaciones de las tablas seleccionadas funcionan correctamente. |
| PT-08 | Login | Los usuarios pueden autenticarse según la configuración. |
| PT-09 | Permisos | Los roles no pueden acceder a funcionalidades restringidas. |
| PT-10 | Dashboard | Las visualizaciones presentan resultados correctos y filtros funcionales. |
| PT-11 | Integración | Todas las funcionalidades trabajan sobre la misma BD. |
| PT-12 | Docker | La aplicación y la base de datos se levantan y funcionan correctamente. |

---

## 10. Criterios de aceptación
El proyecto se considerará funcionalmente completo cuando se cumpla lo siguiente:
### Base de datos
- [ ] MERE corregido y documentado.
- [ ] Modelo relacional consistente con el MERE.
- [ ] Tablas y atributos definidos.
- [ ] PK y FK correctamente implementadas.
- [ ] Restricciones justificadas.
- [ ] Script integral ejecutable desde cero.
### Datos
- [ ] Datos sintéticos suficientes.
- [ ] Datos reproducibles.
- [ ] Integridad referencial.
- [ ] Datos capaces de validar los doce requerimientos SQL y dashboard.
### SQL
- [ ] Seis vistas implementadas.
- [ ] Seis procedimientos implementados.
- [ ] R1–R12 ejecutados y validados.
- [ ] Evidencias documentadas en el informe.
### PMV
- [ ] Formulario transaccional funcional.
- [ ] CRUD funcional en al menos dos tablas.
- [ ] Inicio de sesión funcional.
- [ ] Al menos dos roles con permisos diferenciados.
- [ ] Dashboard con cuatro preguntas de negocio.
- [ ] PMV integrado con la BD del proyecto.
### Arquitectura y despliegue
- [ ] Separación de presentación, lógica y acceso a datos.
- [ ] Consultas parametrizadas.
- [ ] Manejo básico de errores.
- [ ] `requirements.txt`.
- [ ] `Dockerfile`.
- [ ] `docker-compose.yml`.
- [ ] Aplicación ejecutable mediante Docker Compose.
### Documentación y equipo
- [ ] Informe final completo.
- [ ] Matriz de responsabilidades.
- [ ] Bitácoras individuales.
- [ ] Evidencias de ejecución.
- [ ] Presentación preparada.
- [ ] Todos los integrantes preparados para la defensa.

---

## 11. Decisiones pendientes
Todas las decisiones del registro `DECISIONES_DISENO.md` se encuentran pendientes. No se consideran aprobadas en este SPEC.
| ID | Decisión pendiente | Impacto |
|---|---|---|
| DD-01 | Administración y compartición territorial de parques. | MERE, relaciones, FK y modelo relacional. |
| DD-02 | Roles, funciones del personal y cuentas de usuario del PMV. | Personal, modelo de usuarios, R8 y autenticación. |
| DD-03 | Claves e integridad de inscripciones, asistencia y evaluaciones. | PK, FK, UNIQUE, CHECK, consultas y transacciones. |
| DD-04 | Operación exacta del formulario transaccional. | Flujo PMV y lógica de negocio. |
| DD-05 | Tablas que tendrá el CRUD y política de eliminación/desactivación. | Modelo, operaciones y restricciones. |
| DD-06 | Roles y matriz de permisos del PMV. | Accesos y seguridad de la aplicación. |
| DD-07 | Cuarta pregunta de negocio del dashboard. | SQL, visualización y justificación de negocio. |
| DD-08 | Estrategia de poblamiento y volúmenes definitivos de datos. | Generador de datos y validación. |
| DD-09 | Distribución de responsabilidades del equipo. | Matriz, bitácoras y trazabilidad del trabajo. |
### Decisiones que requieren aclaración docente
- **DD-01:** Existen diferencias entre la administración de parques por comunidades autónomas, la compartición territorial y la relación de administración por trabajador presente en el modelo relacional de Fase 1.
- **DD-02:** Se debe aclarar cómo relacionar las funciones operativas del personal, los roles existentes en el modelo y las cuentas de usuario con permisos diferenciados exigidas para el PMV.

---

## 12. Estado y actualización del SPEC
Este documento se considera un borrador de especificación y deberá actualizarse cuando el equipo confirme decisiones de diseño.
Las decisiones aprobadas deberán reflejarse en:
- El registro `DECISIONES_DISENO.md`.
- El MERE.
- El modelo relacional.
- Este `SPEC.md`.
- Los scripts SQL.
- El código del PMV.
- Las pruebas.
- El informe final.

El SPEC deberá mantenerse como referencia principal del proyecto, evitando contradicciones entre los requisitos, el modelo, la implementación y la documentación.

---

## 13. Referencias documentales
- Enunciado oficial de Proyecto Fase 2 — Caso 1.
- Informe de Fase 1 — Grupo 1.
- Rúbrica del Proyecto Fase 2.
- Registro `DECISIONES_DISENO.md`.
- Registro de decisiones pendientes.
