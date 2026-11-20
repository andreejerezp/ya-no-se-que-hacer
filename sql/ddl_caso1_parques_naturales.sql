-- Caso 1: Sistema Integral de Gestión de Parques Naturales
-- Modelo relacional propuesto para MySQL 8.0+
-- Reproducible: elimina y recrea la base de datos.
-- NOTA: decisiones DD-01/DD-02 y algunas reglas de dominio requieren ratificación.

DROP DATABASE IF EXISTS caso1_parques_naturales;
CREATE DATABASE caso1_parques_naturales
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;
USE caso1_parques_naturales;

-- 1) Entidades base
CREATE TABLE ROL (
    idRol INT AUTO_INCREMENT PRIMARY KEY,
    nombreRol VARCHAR(80) NOT NULL,
    CONSTRAINT uq_rol_nombre UNIQUE (nombreRol)
) ENGINE=InnoDB;

CREATE TABLE COMUNIDAD_AUTONOMA (
    codigoComunidad VARCHAR(12) PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    organismoResp VARCHAR(180),
    regionAdmin VARCHAR(120),
    CONSTRAINT uq_comunidad_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE PARQUE_NATURAL (
    numCorrelativo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(160) NOT NULL,
    superficie DECIMAL(12,2) NOT NULL,
    fechaDeclaracion DATE,
    anioDeclaracion SMALLINT,
    estadoConservacion VARCHAR(40),
    presupuesto DECIMAL(14,2),
    idTrabajadorAdministrador INT NULL,
    CONSTRAINT uq_parque_nombre UNIQUE (nombre),
    CONSTRAINT chk_parque_superficie CHECK (superficie > 0),
    CONSTRAINT chk_parque_presupuesto CHECK (presupuesto IS NULL OR presupuesto >= 0),
    CONSTRAINT chk_parque_anio CHECK (anioDeclaracion IS NULL OR anioDeclaracion BETWEEN 1800 AND 2200)
) ENGINE=InnoDB;

CREATE TABLE TRABAJADOR (
    idTrabajador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(160) NOT NULL,
    direccion VARCHAR(240),
    fechaNacimiento DATE,
    estadoCuenta VARCHAR(30),
    idRol INT NOT NULL,
    idSupervisor INT NULL,
    numCorrelativo INT NOT NULL,
    CONSTRAINT fk_trabajador_rol FOREIGN KEY (idRol) REFERENCES ROL(idRol),
    CONSTRAINT fk_trabajador_supervisor FOREIGN KEY (idSupervisor) REFERENCES TRABAJADOR(idTrabajador),
    CONSTRAINT chk_trabajador_no_autosupervisor CHECK (idSupervisor IS NULL OR idSupervisor <> idTrabajador)
) ENGINE=InnoDB;

-- La relación trabajador-trabaja-en y parque-administrador genera referencia circular.
-- Se añade después de crear ambas tablas. Un trabajador puede trabajar en un parque.
ALTER TABLE TRABAJADOR
  ADD CONSTRAINT fk_trabajador_parque FOREIGN KEY (numCorrelativo) REFERENCES PARQUE_NATURAL(numCorrelativo);
ALTER TABLE PARQUE_NATURAL
  ADD CONSTRAINT uq_parque_administrador UNIQUE (idTrabajadorAdministrador),
  ADD CONSTRAINT fk_parque_administrador FOREIGN KEY (idTrabajadorAdministrador) REFERENCES TRABAJADOR(idTrabajador);


-- 2) Atributos multivaluados de trabajador
CREATE TABLE TRABAJADOR_FUNCIONES (
    idTrabajador INT NOT NULL,
    funcion VARCHAR(100) NOT NULL,
    PRIMARY KEY (idTrabajador, funcion),
    CONSTRAINT fk_funcion_trabajador FOREIGN KEY (idTrabajador) REFERENCES TRABAJADOR(idTrabajador) ON DELETE CASCADE
) ENGINE=InnoDB;


CREATE TABLE TRABAJADOR_CONTACTO (
    idTrabajador INT NOT NULL,
    datoContacto VARCHAR(180) NOT NULL,
    PRIMARY KEY (idTrabajador, datoContacto),
    CONSTRAINT fk_contacto_trabajador FOREIGN KEY (idTrabajador) REFERENCES TRABAJADOR(idTrabajador) ON DELETE CASCADE
) ENGINE=InnoDB;


-- 3) Relaciones comunidad-parque y proyectos científicos
CREATE TABLE COMPARTEN (
    numCorrelativo INT NOT NULL,
    codigoComunidad VARCHAR(12) NOT NULL,
    porcentajeTerritorial DECIMAL(5,2) NOT NULL,
    PRIMARY KEY (numCorrelativo, codigoComunidad),
    CONSTRAINT fk_comparten_parque FOREIGN KEY (numCorrelativo) REFERENCES PARQUE_NATURAL(numCorrelativo),
    CONSTRAINT fk_comparten_comunidad FOREIGN KEY (codigoComunidad) REFERENCES COMUNIDAD_AUTONOMA(codigoComunidad),
    CONSTRAINT chk_comparten_porcentaje CHECK (porcentajeTerritorial > 0 AND porcentajeTerritorial <= 100)
) ENGINE=InnoDB;

CREATE TABLE PROYECTO_CIENTIFICO (
    idProyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(180) NOT NULL,
    objetivo TEXT,
    numCorrelativo INT NOT NULL,
    CONSTRAINT fk_proyecto_parque FOREIGN KEY (numCorrelativo) REFERENCES PARQUE_NATURAL(numCorrelativo),
    CONSTRAINT uq_proyecto_parque_nombre UNIQUE (numCorrelativo, nombre)
) ENGINE=InnoDB;

CREATE TABLE PARTICIPA (
    idTrabajador INT NOT NULL,
    idProyecto INT NOT NULL,
    PRIMARY KEY (idTrabajador, idProyecto),
    CONSTRAINT fk_participa_trabajador FOREIGN KEY (idTrabajador) REFERENCES TRABAJADOR(idTrabajador),
    CONSTRAINT fk_participa_proyecto FOREIGN KEY (idProyecto) REFERENCES PROYECTO_CIENTIFICO(idProyecto)
) ENGINE=InnoDB;


-- 4) Especie y especialización parcial/disjunta (disyunción requiere validación adicional)
CREATE TABLE ESPECIE (
    idEspecie INT AUTO_INCREMENT PRIMARY KEY,
    estadoConservacion VARCHAR(40),
    fechaIncorporacion DATE,
    nombreVulgar VARCHAR(160),
    denominacionCientifica VARCHAR(180) NOT NULL,
    CONSTRAINT uq_especie_denominacion UNIQUE (denominacionCientifica)
) ENGINE=InnoDB;

CREATE TABLE VEGETAL (
    idEspecie INT PRIMARY KEY,
    floracion VARCHAR(120),
    CONSTRAINT fk_vegetal_especie FOREIGN KEY (idEspecie) REFERENCES ESPECIE(idEspecie) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE ANIMAL (
    idEspecie INT PRIMARY KEY,
    alimentacion VARCHAR(160),
    periodoCelo VARCHAR(120),
    CONSTRAINT fk_animal_especie FOREIGN KEY (idEspecie) REFERENCES ESPECIE(idEspecie) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE MINERAL (
    idEspecie INT PRIMARY KEY,
    caracteristicasMineral TEXT,
    rocas VARCHAR(180),
    cristales VARCHAR(180),
    CONSTRAINT fk_mineral_especie FOREIGN KEY (idEspecie) REFERENCES ESPECIE(idEspecie) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE INVESTIGA (
    idProyecto INT NOT NULL,
    idEspecie INT NOT NULL,
    PRIMARY KEY (idProyecto, idEspecie),
    CONSTRAINT fk_investiga_proyecto FOREIGN KEY (idProyecto) REFERENCES PROYECTO_CIENTIFICO(idProyecto),
    CONSTRAINT fk_investiga_especie FOREIGN KEY (idEspecie) REFERENCES ESPECIE(idEspecie)
) ENGINE=InnoDB;


-- 5) Área (entidad débil: PK incluye la clave del parque) y proyecto-área
CREATE TABLE AREA (
    numCorrelativo INT NOT NULL,
    numInterno INT NOT NULL,
    nombre VARCHAR(140) NOT NULL,
    estadoOperativo VARCHAR(40),
    nivelAcceso VARCHAR(60),
    extension DECIMAL(12,2),
    PRIMARY KEY (numCorrelativo, numInterno),
    CONSTRAINT fk_area_parque FOREIGN KEY (numCorrelativo) REFERENCES PARQUE_NATURAL(numCorrelativo),
    CONSTRAINT chk_area_numinterno CHECK (numInterno > 0),
    CONSTRAINT chk_area_extension CHECK (extension IS NULL OR extension > 0),
    CONSTRAINT uq_area_nombre_parque UNIQUE (numCorrelativo, nombre)
) ENGINE=InnoDB;


CREATE TABLE SE_DESARROLLA_EN (
    idProyecto INT NOT NULL,
    numCorrelativo INT NOT NULL,
    numInterno INT NOT NULL,
    PRIMARY KEY (idProyecto, numCorrelativo, numInterno),
    CONSTRAINT fk_desarrolla_proyecto FOREIGN KEY (idProyecto) REFERENCES PROYECTO_CIENTIFICO(idProyecto),
    CONSTRAINT fk_desarrolla_area FOREIGN KEY (numCorrelativo, numInterno) REFERENCES AREA(numCorrelativo, numInterno)
) ENGINE=InnoDB;


-- 6) Inventarios y excursiones (excursión débil respecto de área)
CREATE TABLE INVENTARIO_ESPECIE (
    codigoInventario INT AUTO_INCREMENT PRIMARY KEY,
    cantidadInventario INT NOT NULL,
    fechaUltimoMonitoreo DATE,
    observaciones TEXT,
    idEspecie INT NOT NULL,
    numCorrelativo INT NOT NULL,
    numInterno INT NOT NULL,
    CONSTRAINT fk_inventario_especie FOREIGN KEY (idEspecie) REFERENCES ESPECIE(idEspecie),
    CONSTRAINT fk_inventario_area FOREIGN KEY (numCorrelativo, numInterno) REFERENCES AREA(numCorrelativo, numInterno),
    CONSTRAINT chk_inventario_cantidad CHECK (cantidadInventario >= 0)
) ENGINE=InnoDB;

CREATE TABLE EXCURSION (
    numCorrelativo INT NOT NULL,
    numInterno INT NOT NULL,
    codigoExcursion INT NOT NULL,
    modalidad VARCHAR(80) NOT NULL,
    horario VARCHAR(80) NOT NULL,
    fecha DATE NOT NULL,
    capacidad INT NOT NULL,
    PRIMARY KEY (numCorrelativo, numInterno, codigoExcursion),
    CONSTRAINT fk_excursion_area FOREIGN KEY (numCorrelativo, numInterno) REFERENCES AREA(numCorrelativo, numInterno),
    CONSTRAINT chk_excursion_codigo CHECK (codigoExcursion > 0),
    CONSTRAINT chk_excursion_capacidad CHECK (capacidad > 0)
) ENGINE=InnoDB;


-- 7) Visitantes, inscripción y evaluación
CREATE TABLE VISITANTE (
    idVisitante INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(160) NOT NULL,
    contacto VARCHAR(180),
    fechaNacimiento DATE
) ENGINE=InnoDB;

CREATE TABLE INSCRIPCION (
    idInscripcion INT AUTO_INCREMENT PRIMARY KEY,
    numCorrelativo INT NOT NULL,
    numInterno INT NOT NULL,
    codigoExcursion INT NOT NULL,
    idVisitante INT NOT NULL,
    asistencia VARCHAR(30) NOT NULL DEFAULT 'Pendiente',
    observaciones TEXT,
    CONSTRAINT fk_inscripcion_excursion FOREIGN KEY (numCorrelativo, numInterno, codigoExcursion) REFERENCES EXCURSION(numCorrelativo, numInterno, codigoExcursion),
    CONSTRAINT fk_inscripcion_visitante FOREIGN KEY (idVisitante) REFERENCES VISITANTE(idVisitante),
    CONSTRAINT uq_inscripcion_visitante_excursion UNIQUE (numCorrelativo, numInterno, codigoExcursion, idVisitante),
    CONSTRAINT chk_inscripcion_asistencia CHECK (asistencia IN ('Pendiente', 'Asistio', 'No asistio', 'Cancelada'))
) ENGINE=InnoDB;

CREATE TABLE EVALUACION (
    idInscripcion INT PRIMARY KEY,
    numCorrelativoEval INT,
    fecha DATE NOT NULL,
    calificacion DECIMAL(3,1) NOT NULL,
    comentario TEXT,
    CONSTRAINT fk_evaluacion_inscripcion FOREIGN KEY (idInscripcion) REFERENCES INSCRIPCION(idInscripcion) ON DELETE CASCADE,
    CONSTRAINT uq_evaluacion_folio UNIQUE (numCorrelativoEval),
    CONSTRAINT chk_evaluacion_calificacion CHECK (calificacion BETWEEN 1 AND 7)
) ENGINE=InnoDB;

-- Fin del DDL. Este archivo crea únicamente el esquema relacional; no incluye datos,
-- vistas, procedimientos almacenados ni aplicación Streamlit.
