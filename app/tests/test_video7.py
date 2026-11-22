from datetime import date
from sqlalchemy import text
from db.connection import engine, wait_for_database
from services.catalogo_service import (
    actualizar_especie_catalogo,
    actualizar_parque_natural,
    crear_especie_catalogo,
    crear_parque_natural,
    eliminar_especie_catalogo,
    eliminar_parque_natural,
    obtener_especies,
    obtener_parques,
)
from services.inscripcion_service import (
    get_formulario_inscripcion_options,
    registrar_inscripcion_excursion,
)


def run_checks() -> None:
    wait_for_database()
    visitantes, excursiones = get_formulario_inscripcion_options()
    assert len(visitantes) > 0, "Debe existir al menos un visitante en VISITANTE."
    assert len(excursiones) > 0, "Debe existir al menos una excursión en EXCURSION."

    id_vis = visitantes[0]["idVisitante"]
    exc = excursiones[0]
    ok_ins, msg_ins = registrar_inscripcion_excursion(
        id_visitante=id_vis,
        num_correlativo=exc["numCorrelativo"],
        num_interno=exc["numInterno"],
        codigo_excursion=exc["codigoExcursion"],
        asistencia="Pendiente",
        observaciones="Prueba automatizada Video 7",
    )
    print("Inscripción 1:", ok_ins, msg_ins)

    # Intentar duplicado
    ok_dup, msg_dup = registrar_inscripcion_excursion(
        id_visitante=id_vis,
        num_correlativo=exc["numCorrelativo"],
        num_interno=exc["numInterno"],
        codigo_excursion=exc["codigoExcursion"],
        asistencia="Pendiente",
        observaciones="Duplicado",
    )
    print("Duplicado esperado False:", ok_dup, msg_dup)
    assert not ok_dup, "No debe permitir duplicar visitante en la misma excursión."

    # Limpiar inscripción de prueba
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                DELETE FROM INSCRIPCION
                WHERE idVisitante = :vid
                  AND numCorrelativo = :nc
                  AND numInterno = :ni
                  AND codigoExcursion = :ce
                  AND observaciones = 'Prueba automatizada Video 7'
                """
            ),
            {
                "vid": id_vis,
                "nc": exc["numCorrelativo"],
                "ni": exc["numInterno"],
                "ce": exc["codigoExcursion"],
            },
        )

    # CRUD Parque Natural
    ok_cp, msg_cp = crear_parque_natural(
        nombre="Parque Prueba Video 7",
        superficie_raw="500.50",
        fecha_declaracion=date(2020, 5, 10),
        anio_declaracion=2020,
        estado_conservacion="Bueno",
        presupuesto_raw="100000.00",
        id_trabajador_admin=None,
    )
    print("Crear parque:", ok_cp, msg_cp)
    assert ok_cp
    creados_p = obtener_parques(filtro_texto="Parque Prueba Video 7")
    assert len(creados_p) == 1
    pid = creados_p[0]["numCorrelativo"]

    ok_up, msg_up = actualizar_parque_natural(
        num_correlativo=pid,
        nombre="Parque Prueba Video 7 Editado",
        superficie_raw="750.00",
        fecha_declaracion=date(2020, 5, 10),
        anio_declaracion=2020,
        estado_conservacion="Óptimo",
        presupuesto_raw="150000.00",
        id_trabajador_admin=None,
    )
    print("Actualizar parque:", ok_up, msg_up)
    assert ok_up

    ok_dp, msg_dp = eliminar_parque_natural(pid)
    print("Eliminar parque:", ok_dp, msg_dp)
    assert ok_dp

    # CRUD Especie
    ok_ce, msg_ce = crear_especie_catalogo(
        denominacion_cientifica="Nothofagus prueba_v7",
        nombre_vulgar="Árbol Prueba",
        estado_conservacion="Vulnerable",
        fecha_incorporacion=date(2024, 1, 15),
        tipo_especie="Vegetal",
        floracion="Primavera",
    )
    print("Crear especie:", ok_ce, msg_ce)
    assert ok_ce
    creadas_e = obtener_especies(filtro_texto="Nothofagus prueba_v7")
    assert len(creadas_e) == 1
    eid = creadas_e[0]["idEspecie"]

    ok_ue, msg_ue = actualizar_especie_catalogo(
        id_especie=eid,
        denominacion_cientifica="Nothofagus prueba_v7",
        nombre_vulgar="Árbol Prueba Editado",
        estado_conservacion="En recuperación",
        fecha_incorporacion=date(2024, 1, 15),
        tipo_especie="Animal",
        alimentacion="Herbívoro",
        periodo_celo="Otoño",
    )
    print("Actualizar especie:", ok_ue, msg_ue)
    assert ok_ue

    ok_de, msg_de = eliminar_especie_catalogo(eid)
    print("Eliminar especie:", ok_de, msg_de)
    assert ok_de
    print("Todas las comprobaciones de Video 7 pasaron correctamente.")


if __name__ == "__main__":
    run_checks()
