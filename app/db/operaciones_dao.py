from datetime import date
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from .connection import engine


def list_visitors_for_select() -> list[dict]:
    query = text(
        """
        SELECT idVisitante, nombre, contacto
        FROM VISITANTE
        ORDER BY nombre ASC, idVisitante ASC
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
    return [dict(r) for r in rows]


def list_excursions_for_select() -> list[dict]:
    query = text(
        """
        SELECT
            e.numCorrelativo,
            e.numInterno,
            e.codigoExcursion,
            e.modalidad,
            e.horario,
            e.fecha,
            e.capacidad,
            a.nombre AS nombreArea,
            p.nombre AS nombreParque,
            COALESCE(ins.activos, 0) AS inscritosActivos
        FROM EXCURSION e
        INNER JOIN AREA a
            ON a.numCorrelativo = e.numCorrelativo
           AND a.numInterno = e.numInterno
        INNER JOIN PARQUE_NATURAL p
            ON p.numCorrelativo = e.numCorrelativo
        LEFT JOIN (
            SELECT
                numCorrelativo,
                numInterno,
                codigoExcursion,
                COUNT(*) AS activos
            FROM INSCRIPCION
            WHERE asistencia <> 'Cancelada'
            GROUP BY numCorrelativo, numInterno, codigoExcursion
        ) ins
            ON ins.numCorrelativo = e.numCorrelativo
           AND ins.numInterno = e.numInterno
           AND ins.codigoExcursion = e.codigoExcursion
        ORDER BY e.fecha DESC, p.nombre ASC, a.nombre ASC, e.codigoExcursion ASC
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query).mappings().all()
    return [dict(r) for r in rows]


def get_excursion_capacity_info(
    num_correlativo: int, num_interno: int, codigo_excursion: int
) -> dict | None:
    query = text(
        """
        SELECT
            e.numCorrelativo,
            e.numInterno,
            e.codigoExcursion,
            e.capacidad,
            COALESCE(ins.activos, 0) AS inscritosActivos
        FROM EXCURSION e
        LEFT JOIN (
            SELECT
                numCorrelativo,
                numInterno,
                codigoExcursion,
                COUNT(*) AS activos
            FROM INSCRIPCION
            WHERE asistencia <> 'Cancelada'
            GROUP BY numCorrelativo, numInterno, codigoExcursion
        ) ins
            ON ins.numCorrelativo = e.numCorrelativo
           AND ins.numInterno = e.numInterno
           AND ins.codigoExcursion = e.codigoExcursion
        WHERE e.numCorrelativo = :num_correlativo
          AND e.numInterno = :num_interno
          AND e.codigoExcursion = :codigo_excursion
        """
    )
    with engine.connect() as conn:
        row = (
            conn.execute(
                query,
                {
                    "num_correlativo": num_correlativo,
                    "num_interno": num_interno,
                    "codigo_excursion": codigo_excursion,
                },
            )
            .mappings()
            .first()
        )
    return dict(row) if row else None


def exists_inscripcion(
    num_correlativo: int, num_interno: int, codigo_excursion: int, id_visitante: int
) -> bool:
    query = text(
        """
        SELECT 1
        FROM INSCRIPCION
        WHERE numCorrelativo = :num_correlativo
          AND numInterno = :num_interno
          AND codigoExcursion = :codigo_excursion
          AND idVisitante = :id_visitante
        LIMIT 1
        """
    )
    with engine.connect() as conn:
        row = conn.execute(
            query,
            {
                "num_correlativo": num_correlativo,
                "num_interno": num_interno,
                "codigo_excursion": codigo_excursion,
                "id_visitante": id_visitante,
            },
        ).first()
    return row is not None


def insert_inscripcion(
    num_correlativo: int,
    num_interno: int,
    codigo_excursion: int,
    id_visitante: int,
    asistencia: str,
    observaciones: str | None,
) -> int:
    insert_sql = text(
        """
        INSERT INTO INSCRIPCION (
            numCorrelativo,
            numInterno,
            codigoExcursion,
            idVisitante,
            asistencia,
            observaciones
        )
        VALUES (
            :num_correlativo,
            :num_interno,
            :codigo_excursion,
            :id_visitante,
            :asistencia,
            :observaciones
        )
        """
    )
    try:
        with engine.begin() as conn:
            result = conn.execute(
                insert_sql,
                {
                    "num_correlativo": num_correlativo,
                    "num_interno": num_interno,
                    "codigo_excursion": codigo_excursion,
                    "id_visitante": id_visitante,
                    "asistencia": asistencia,
                    "observaciones": observaciones,
                },
            )
            return int(result.lastrowid)
    except IntegrityError as exc:
        raise ValueError(f"Error de integridad al registrar inscripción: {exc.orig}") from exc


def list_recent_inscripciones(limit: int = 15) -> list[dict]:
    query = text(
        """
        SELECT
            i.idInscripcion,
            v.nombre AS visitante,
            p.nombre AS parque,
            a.nombre AS area,
            i.codigoExcursion,
            i.asistencia,
            i.observaciones
        FROM INSCRIPCION i
        INNER JOIN VISITANTE v ON v.idVisitante = i.idVisitante
        INNER JOIN PARQUE_NATURAL p ON p.numCorrelativo = i.numCorrelativo
        INNER JOIN AREA a
            ON a.numCorrelativo = i.numCorrelativo
           AND a.numInterno = i.numInterno
        ORDER BY i.idInscripcion DESC
        LIMIT :limite
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query, {"limite": limit}).mappings().all()
    return [dict(r) for r in rows]


def list_administradores_disponibles(incluir_id_actual: int | None = None) -> list[dict]:
    query = text(
        """
        SELECT t.idTrabajador, t.nombre, r.nombreRol
        FROM TRABAJADOR t
        LEFT JOIN ROL r ON r.idRol = t.idRol
        LEFT JOIN PARQUE_NATURAL p ON p.idTrabajadorAdministrador = t.idTrabajador
        WHERE p.numCorrelativo IS NULL
           OR (:id_actual IS NOT NULL AND t.idTrabajador = :id_actual)
        ORDER BY t.nombre ASC
        """
    )
    with engine.connect() as conn:
        rows = conn.execute(query, {"id_actual": incluir_id_actual}).mappings().all()
    return [dict(r) for r in rows]


def list_parques(filtro_texto: str = "", filtro_estado: str = "Todos") -> list[dict]:
    sql = """
        SELECT
            p.numCorrelativo,
            p.nombre,
            p.superficie,
            p.fechaDeclaracion,
            p.anioDeclaracion,
            p.estadoConservacion,
            p.presupuesto,
            p.idTrabajadorAdministrador,
            t.nombre AS nombreAdministrador
        FROM PARQUE_NATURAL p
        LEFT JOIN TRABAJADOR t
            ON t.idTrabajador = p.idTrabajadorAdministrador
        WHERE 1 = 1
    """
    params: dict = {}
    if filtro_texto.strip():
        sql += " AND p.nombre LIKE :texto"
        params["texto"] = f"%{filtro_texto.strip()}%"
    if filtro_estado != "Todos":
        sql += " AND p.estadoConservacion = :estado"
        params["estado"] = filtro_estado
    sql += " ORDER BY p.numCorrelativo ASC"

    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()
    return [dict(r) for r in rows]


def create_parque(
    nombre: str,
    superficie: Decimal,
    fecha_declaracion: date | None,
    anio_declaracion: int | None,
    estado_conservacion: str | None,
    presupuesto: Decimal | None,
    id_trabajador_admin: int | None,
) -> int:
    insert_sql = text(
        """
        INSERT INTO PARQUE_NATURAL (
            nombre,
            superficie,
            fechaDeclaracion,
            anioDeclaracion,
            estadoConservacion,
            presupuesto,
            idTrabajadorAdministrador
        )
        VALUES (
            :nombre,
            :superficie,
            :fecha_declaracion,
            :anio_declaracion,
            :estado_conservacion,
            :presupuesto,
            :id_trabajador_admin
        )
        """
    )
    try:
        with engine.begin() as conn:
            result = conn.execute(
                insert_sql,
                {
                    "nombre": nombre,
                    "superficie": superficie,
                    "fecha_declaracion": fecha_declaracion,
                    "anio_declaracion": anio_declaracion,
                    "estado_conservacion": estado_conservacion,
                    "presupuesto": presupuesto,
                    "id_trabajador_admin": id_trabajador_admin,
                },
            )
            return int(result.lastrowid)
    except IntegrityError as exc:
        raise ValueError(f"No se pudo crear el parque natural: {exc.orig}") from exc


def update_parque(
    num_correlativo: int,
    nombre: str,
    superficie: Decimal,
    fecha_declaracion: date | None,
    anio_declaracion: int | None,
    estado_conservacion: str | None,
    presupuesto: Decimal | None,
    id_trabajador_admin: int | None,
) -> bool:
    update_sql = text(
        """
        UPDATE PARQUE_NATURAL
        SET
            nombre = :nombre,
            superficie = :superficie,
            fechaDeclaracion = :fecha_declaracion,
            anioDeclaracion = :anio_declaracion,
            estadoConservacion = :estado_conservacion,
            presupuesto = :presupuesto,
            idTrabajadorAdministrador = :id_trabajador_admin
        WHERE numCorrelativo = :num_correlativo
        """
    )
    try:
        with engine.begin() as conn:
            result = conn.execute(
                update_sql,
                {
                    "num_correlativo": num_correlativo,
                    "nombre": nombre,
                    "superficie": superficie,
                    "fecha_declaracion": fecha_declaracion,
                    "anio_declaracion": anio_declaracion,
                    "estado_conservacion": estado_conservacion,
                    "presupuesto": presupuesto,
                    "id_trabajador_admin": id_trabajador_admin,
                },
            )
            return result.rowcount > 0
    except IntegrityError as exc:
        raise ValueError(f"No se pudo actualizar el parque natural: {exc.orig}") from exc


def delete_parque(num_correlativo: int) -> bool:
    delete_sql = text("DELETE FROM PARQUE_NATURAL WHERE numCorrelativo = :num_correlativo")
    try:
        with engine.begin() as conn:
            result = conn.execute(delete_sql, {"num_correlativo": num_correlativo})
            return result.rowcount > 0
    except IntegrityError as exc:
        raise ValueError(
            "FK_RESTRICT: El parque tiene registros relacionados (áreas, trabajadores, proyectos o compartición territorial)."
        ) from exc


def list_especies(filtro_texto: str = "", filtro_tipo: str = "Todos") -> list[dict]:
    sql = """
        SELECT
            e.idEspecie,
            e.denominacionCientifica,
            e.nombreVulgar,
            e.estadoConservacion,
            e.fechaIncorporacion,
            CASE
                WHEN v.idEspecie IS NOT NULL THEN 'Vegetal'
                WHEN a.idEspecie IS NOT NULL THEN 'Animal'
                WHEN m.idEspecie IS NOT NULL THEN 'Mineral'
                ELSE 'Sin clasificar'
            END AS tipoEspecie,
            v.floracion,
            a.alimentacion,
            a.periodoCelo,
            m.caracteristicasMineral,
            m.rocas,
            m.cristales
        FROM ESPECIE e
        LEFT JOIN VEGETAL v ON v.idEspecie = e.idEspecie
        LEFT JOIN ANIMAL a ON a.idEspecie = e.idEspecie
        LEFT JOIN MINERAL m ON m.idEspecie = e.idEspecie
        WHERE 1 = 1
    """
    params: dict = {}
    if filtro_texto.strip():
        sql += " AND (e.denominacionCientifica LIKE :texto OR COALESCE(e.nombreVulgar, '') LIKE :texto)"
        params["texto"] = f"%{filtro_texto.strip()}%"
    if filtro_tipo == "Vegetal":
        sql += " AND v.idEspecie IS NOT NULL"
    elif filtro_tipo == "Animal":
        sql += " AND a.idEspecie IS NOT NULL"
    elif filtro_tipo == "Mineral":
        sql += " AND m.idEspecie IS NOT NULL"
    elif filtro_tipo == "Sin clasificar":
        sql += " AND v.idEspecie IS NULL AND a.idEspecie IS NULL AND m.idEspecie IS NULL"

    sql += " ORDER BY e.idEspecie ASC"
    with engine.connect() as conn:
        rows = conn.execute(text(sql), params).mappings().all()
    return [dict(r) for r in rows]


def create_especie(
    denominacion_cientifica: str,
    nombre_vulgar: str | None,
    estado_conservacion: str | None,
    fecha_incorporacion: date | None,
    tipo_especie: str,
    floracion: str | None = None,
    alimentacion: str | None = None,
    periodo_celo: str | None = None,
    caracteristicas_mineral: str | None = None,
    rocas: str | None = None,
    cristales: str | None = None,
) -> int:
    insert_especie = text(
        """
        INSERT INTO ESPECIE (
            denominacionCientifica,
            nombreVulgar,
            estadoConservacion,
            fechaIncorporacion
        )
        VALUES (
            :denominacion_cientifica,
            :nombre_vulgar,
            :estado_conservacion,
            :fecha_incorporacion
        )
        """
    )
    try:
        with engine.begin() as conn:
            res = conn.execute(
                insert_especie,
                {
                    "denominacion_cientifica": denominacion_cientifica,
                    "nombre_vulgar": nombre_vulgar,
                    "estado_conservacion": estado_conservacion,
                    "fecha_incorporacion": fecha_incorporacion,
                },
            )
            id_especie = int(res.lastrowid)

            if tipo_especie == "Vegetal":
                conn.execute(
                    text("INSERT INTO VEGETAL (idEspecie, floracion) VALUES (:id, :floracion)"),
                    {"id": id_especie, "floracion": floracion},
                )
            elif tipo_especie == "Animal":
                conn.execute(
                    text(
                        "INSERT INTO ANIMAL (idEspecie, alimentacion, periodoCelo) "
                        "VALUES (:id, :alimentacion, :periodo_celo)"
                    ),
                    {
                        "id": id_especie,
                        "alimentacion": alimentacion,
                        "periodo_celo": periodo_celo,
                    },
                )
            elif tipo_especie == "Mineral":
                conn.execute(
                    text(
                        "INSERT INTO MINERAL (idEspecie, caracteristicasMineral, rocas, cristales) "
                        "VALUES (:id, :caract, :rocas, :cristales)"
                    ),
                    {
                        "id": id_especie,
                        "caract": caracteristicas_mineral,
                        "rocas": rocas,
                        "cristales": cristales,
                    },
                )

            return id_especie
    except IntegrityError as exc:
        raise ValueError(f"No se pudo crear la especie: {exc.orig}") from exc


def update_especie(
    id_especie: int,
    denominacion_cientifica: str,
    nombre_vulgar: str | None,
    estado_conservacion: str | None,
    fecha_incorporacion: date | None,
    tipo_especie: str,
    floracion: str | None = None,
    alimentacion: str | None = None,
    periodo_celo: str | None = None,
    caracteristicas_mineral: str | None = None,
    rocas: str | None = None,
    cristales: str | None = None,
) -> bool:
    update_sql = text(
        """
        UPDATE ESPECIE
        SET
            denominacionCientifica = :denominacion_cientifica,
            nombreVulgar = :nombre_vulgar,
            estadoConservacion = :estado_conservacion,
            fechaIncorporacion = :fecha_incorporacion
        WHERE idEspecie = :id_especie
        """
    )
    try:
        with engine.begin() as conn:
            res = conn.execute(
                update_sql,
                {
                    "id_especie": id_especie,
                    "denominacion_cientifica": denominacion_cientifica,
                    "nombre_vulgar": nombre_vulgar,
                    "estado_conservacion": estado_conservacion,
                    "fecha_incorporacion": fecha_incorporacion,
                },
            )
            if res.rowcount == 0:
                return False

            conn.execute(text("DELETE FROM VEGETAL WHERE idEspecie = :id"), {"id": id_especie})
            conn.execute(text("DELETE FROM ANIMAL WHERE idEspecie = :id"), {"id": id_especie})
            conn.execute(text("DELETE FROM MINERAL WHERE idEspecie = :id"), {"id": id_especie})

            if tipo_especie == "Vegetal":
                conn.execute(
                    text("INSERT INTO VEGETAL (idEspecie, floracion) VALUES (:id, :floracion)"),
                    {"id": id_especie, "floracion": floracion},
                )
            elif tipo_especie == "Animal":
                conn.execute(
                    text(
                        "INSERT INTO ANIMAL (idEspecie, alimentacion, periodoCelo) "
                        "VALUES (:id, :alimentacion, :periodo_celo)"
                    ),
                    {
                        "id": id_especie,
                        "alimentacion": alimentacion,
                        "periodo_celo": periodo_celo,
                    },
                )
            elif tipo_especie == "Mineral":
                conn.execute(
                    text(
                        "INSERT INTO MINERAL (idEspecie, caracteristicasMineral, rocas, cristales) "
                        "VALUES (:id, :caract, :rocas, :cristales)"
                    ),
                    {
                        "id": id_especie,
                        "caract": caracteristicas_mineral,
                        "rocas": rocas,
                        "cristales": cristales,
                    },
                )

            return True
    except IntegrityError as exc:
        raise ValueError(f"No se pudo actualizar la especie: {exc.orig}") from exc


def delete_especie(id_especie: int) -> bool:
    delete_sql = text("DELETE FROM ESPECIE WHERE idEspecie = :id_especie")
    try:
        with engine.begin() as conn:
            res = conn.execute(delete_sql, {"id_especie": id_especie})
            return res.rowcount > 0
    except IntegrityError as exc:
        raise ValueError(
            "FK_RESTRICT: La especie está referenciada en INVENTARIO_ESPECIE o INVESTIGA."
        ) from exc
