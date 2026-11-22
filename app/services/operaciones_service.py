from datetime import date
from decimal import Decimal, InvalidOperation
from db.operaciones_dao import (
    create_especie,
    create_parque,
    delete_especie,
    delete_parque,
    exists_inscripcion,
    get_excursion_capacity_info,
    insert_inscripcion,
    list_administradores_disponibles,
    list_especies,
    list_excursions_for_select,
    list_parques,
    list_recent_inscripciones,
    list_visitors_for_select,
    update_especie,
    update_parque,
)

ESTADOS_ASISTENCIA_VALIDOS = ("Pendiente", "Asistio", "No asistio", "Cancelada")
TIPOS_ESPECIE = ("Sin clasificar", "Vegetal", "Animal", "Mineral")


def _parse_optional_decimal(valor: str | float | int | None, campo: str) -> Decimal | None:
    if valor is None:
        return None
    texto = str(valor).strip()
    if texto == "":
        return None
    try:
        return Decimal(texto)
    except InvalidOperation as exc:
        raise ValueError(f"El campo '{campo}' debe ser un número válido.") from exc


def _clean_optional_text(valor: str | None) -> str | None:
    if valor is None:
        return None
    limpio = valor.strip()
    return limpio if limpio else None


def get_formulario_inscripcion_options() -> tuple[list[dict], list[dict]]:
    return list_visitors_for_select(), list_excursions_for_select()


def registrar_inscripcion_excursion(
    id_visitante: int,
    num_correlativo: int,
    num_interno: int,
    codigo_excursion: int,
    asistencia: str,
    observaciones: str | None,
) -> tuple[bool, str]:
    if not id_visitante or id_visitante <= 0:
        return False, "Debes seleccionar un visitante válido."
    if asistencia not in ESTADOS_ASISTENCIA_VALIDOS:
        return False, f"Estado de asistencia no válido. Valores permitidos: {', '.join(ESTADOS_ASISTENCIA_VALIDOS)}."

    excursion = get_excursion_capacity_info(num_correlativo, num_interno, codigo_excursion)
    if excursion is None:
        return False, "La excursión seleccionada no existe en el catálogo."

    if exists_inscripcion(num_correlativo, num_interno, codigo_excursion, id_visitante):
        return False, "El visitante ya está inscrito en esta excursión."

    if asistencia != "Cancelada" and int(excursion["inscritosActivos"]) >= int(excursion["capacidad"]):
        return (
            False,
            f"La excursión alcanzó su capacidad máxima ({excursion['inscritosActivos']}/{excursion['capacidad']}).",
        )

    obs_limpia = _clean_optional_text(observaciones)
    try:
        nuevo_id = insert_inscripcion(
            num_correlativo=num_correlativo,
            num_interno=num_interno,
            codigo_excursion=codigo_excursion,
            id_visitante=id_visitante,
            asistencia=asistencia,
            observaciones=obs_limpia,
        )
        return True, f"Inscripción registrada correctamente con ID #{nuevo_id}."
    except ValueError as exc:
        return False, str(exc)


def obtener_ultimas_inscripciones(limit: int = 15) -> list[dict]:
    return list_recent_inscripciones(limit=limit)


def obtener_parques(filtro_texto: str = "", filtro_estado: str = "Todos") -> list[dict]:
    return list_parques(filtro_texto=filtro_texto, filtro_estado=filtro_estado)


def obtener_administradores(incluir_id_actual: int | None = None) -> list[dict]:
    return list_administradores_disponibles(incluir_id_actual=incluir_id_actual)


def crear_parque_natural(
    nombre: str,
    superficie_raw: str | float,
    fecha_declaracion: date | None,
    anio_declaracion: int | None,
    estado_conservacion: str | None,
    presupuesto_raw: str | float | None,
    id_trabajador_admin: int | None,
) -> tuple[bool, str]:
    nombre_limpio = (nombre or "").strip()
    if not nombre_limpio:
        return False, "El nombre del parque natural es obligatorio."

    try:
        superficie = _parse_optional_decimal(superficie_raw, "Superficie")
        if superficie is None or superficie <= 0:
            return False, "La superficie debe ser mayor que 0."
        presupuesto = _parse_optional_decimal(presupuesto_raw, "Presupuesto")
        if presupuesto is not None and presupuesto < 0:
            return False, "El presupuesto no puede ser negativo."
        if anio_declaracion is not None and not (1800 <= anio_declaracion <= 2200):
            return False, "El año de declaración debe estar entre 1800 y 2200."

        nuevo_id = create_parque(
            nombre=nombre_limpio,
            superficie=superficie,
            fecha_declaracion=fecha_declaracion,
            anio_declaracion=anio_declaracion,
            estado_conservacion=_clean_optional_text(estado_conservacion),
            presupuesto=presupuesto,
            id_trabajador_admin=id_trabajador_admin,
        )
        return True, f"Parque natural creado con numCorrelativo #{nuevo_id}."
    except ValueError as exc:
        return False, str(exc)


def actualizar_parque_natural(
    num_correlativo: int,
    nombre: str,
    superficie_raw: str | float,
    fecha_declaracion: date | None,
    anio_declaracion: int | None,
    estado_conservacion: str | None,
    presupuesto_raw: str | float | None,
    id_trabajador_admin: int | None,
) -> tuple[bool, str]:
    nombre_limpio = (nombre or "").strip()
    if not nombre_limpio:
        return False, "El nombre del parque natural es obligatorio."

    try:
        superficie = _parse_optional_decimal(superficie_raw, "Superficie")
        if superficie is None or superficie <= 0:
            return False, "La superficie debe ser mayor que 0."
        presupuesto = _parse_optional_decimal(presupuesto_raw, "Presupuesto")
        if presupuesto is not None and presupuesto < 0:
            return False, "El presupuesto no puede ser negativo."
        if anio_declaracion is not None and not (1800 <= anio_declaracion <= 2200):
            return False, "El año de declaración debe estar entre 1800 y 2200."

        ok = update_parque(
            num_correlativo=num_correlativo,
            nombre=nombre_limpio,
            superficie=superficie,
            fecha_declaracion=fecha_declaracion,
            anio_declaracion=anio_declaracion,
            estado_conservacion=_clean_optional_text(estado_conservacion),
            presupuesto=presupuesto,
            id_trabajador_admin=id_trabajador_admin,
        )
        if not ok:
            return False, f"No se encontró el parque #{num_correlativo}."
        return True, f"Parque natural #{num_correlativo} actualizado correctamente."
    except ValueError as exc:
        return False, str(exc)


def eliminar_parque_natural(num_correlativo: int) -> tuple[bool, str]:
    try:
        ok = delete_parque(num_correlativo)
        if not ok:
            return False, f"No se encontró el parque #{num_correlativo}."
        return True, f"Parque natural #{num_correlativo} eliminado correctamente."
    except ValueError as exc:
        return (
            False,
            f"No es posible eliminar el parque #{num_correlativo}: {exc}. "
            "Alternativa sin alterar el esquema actual: eliminar o reasignar previamente sus áreas, "
            "trabajadores, proyectos o filas en COMPARTEN, o bien acordar en el equipo añadir una "
            "columna de estado lógico en PARQUE_NATURAL.",
        )


def obtener_especies(filtro_texto: str = "", filtro_tipo: str = "Todos") -> list[dict]:
    return list_especies(filtro_texto=filtro_texto, filtro_tipo=filtro_tipo)


def crear_especie_catalogo(
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
) -> tuple[bool, str]:
    denom_limpia = (denominacion_cientifica or "").strip()
    if not denom_limpia:
        return False, "La denominación científica es obligatoria."
    if tipo_especie not in TIPOS_ESPECIE:
        return False, "Tipo de especie no válido."

    try:
        nuevo_id = create_especie(
            denominacion_cientifica=denom_limpia,
            nombre_vulgar=_clean_optional_text(nombre_vulgar),
            estado_conservacion=_clean_optional_text(estado_conservacion),
            fecha_incorporacion=fecha_incorporacion,
            tipo_especie=tipo_especie,
            floracion=_clean_optional_text(floracion),
            alimentacion=_clean_optional_text(alimentacion),
            periodo_celo=_clean_optional_text(periodo_celo),
            caracteristicas_mineral=_clean_optional_text(caracteristicas_mineral),
            rocas=_clean_optional_text(rocas),
            cristales=_clean_optional_text(cristales),
        )
        return True, f"Especie registrada con idEspecie #{nuevo_id} ({tipo_especie})."
    except ValueError as exc:
        return False, str(exc)


def actualizar_especie_catalogo(
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
) -> tuple[bool, str]:
    denom_limpia = (denominacion_cientifica or "").strip()
    if not denom_limpia:
        return False, "La denominación científica es obligatoria."
    if tipo_especie not in TIPOS_ESPECIE:
        return False, "Tipo de especie no válido."

    try:
        ok = update_especie(
            id_especie=id_especie,
            denominacion_cientifica=denom_limpia,
            nombre_vulgar=_clean_optional_text(nombre_vulgar),
            estado_conservacion=_clean_optional_text(estado_conservacion),
            fecha_incorporacion=fecha_incorporacion,
            tipo_especie=tipo_especie,
            floracion=_clean_optional_text(floracion),
            alimentacion=_clean_optional_text(alimentacion),
            periodo_celo=_clean_optional_text(periodo_celo),
            caracteristicas_mineral=_clean_optional_text(caracteristicas_mineral),
            rocas=_clean_optional_text(rocas),
            cristales=_clean_optional_text(cristales),
        )
        if not ok:
            return False, f"No se encontró la especie #{id_especie}."
        return True, f"Especie #{id_especie} actualizada ({tipo_especie})."
    except ValueError as exc:
        return False, str(exc)


def eliminar_especie_catalogo(id_especie: int) -> tuple[bool, str]:
    try:
        ok = delete_especie(id_especie)
        if not ok:
            return False, f"No se encontró la especie #{id_especie}."
        return True, f"Especie #{id_especie} eliminada correctamente."
    except ValueError as exc:
        return (
            False,
            f"No es posible eliminar la especie #{id_especie}: {exc}. "
            "Alternativa sin alterar el esquema actual: eliminar primero los registros asociados "
            "en INVENTARIO_ESPECIE o INVESTIGA (los subtipos VEGETAL/ANIMAL/MINERAL se eliminan en cascada).",
        )
