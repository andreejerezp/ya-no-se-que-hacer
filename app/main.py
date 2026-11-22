from datetime import date
import streamlit as st
from db.connection import wait_for_database
from services.operaciones_service import (
    ESTADOS_ASISTENCIA_VALIDOS,
    TIPOS_ESPECIE,
    actualizar_especie_catalogo,
    actualizar_parque_natural,
    crear_especie_catalogo,
    crear_parque_natural,
    eliminar_especie_catalogo,
    eliminar_parque_natural,
    get_formulario_inscripcion_options,
    obtener_administradores,
    obtener_especies,
    obtener_parques,
    obtener_ultimas_inscripciones,
    registrar_inscripcion_excursion,
)
from services.metrics_service import get_home_metrics

st.set_page_config(page_title="Parques Naturales", page_icon="🌿", layout="wide")

st.title("🌿 Sistema Integral de Gestión de Parques Naturales")
st.write("Aplicación inicial del PMV — Caso 1, Fase 2.")
st.caption("Conexión real a MySQL mediante SQLAlchemy + PyMySQL.")

try:
    wait_for_database()
    metrics = get_home_metrics()
    col1, col2 = st.columns(2)
    col1.metric("Visitantes registrados", metrics["visitantes"])
    col2.metric("Excursiones registradas", metrics["excursiones"])
    st.success("Conexión a MySQL exitosa y consultas ejecutadas.")
except Exception as exc:
    st.error(
        "No se pudo conectar o consultar MySQL. Verifica que el contenedor db esté activo "
        "y que las variables de entorno coincidan."
    )
    st.info("La aplicación reintenta la conexión durante un período limitado al iniciar.")
    st.exception(exc)
    st.stop()

st.divider()

tab_inscripcion, tab_parques, tab_especies = st.tabs(
    [
        "🧭 Inscripción a Excursión",
        "🏞️ CRUD Parque Natural",
        "🌱 CRUD Especie",
    ]
)

with tab_inscripcion:
    st.subheader("Registrar inscripción de visitante a excursión")
    visitantes, excursiones = get_formulario_inscripcion_options()

    if not visitantes or not excursiones:
        st.warning("Se requieren visitantes y excursiones registradas en la base de datos para inscribir.")
    else:
        visitante_map = {
            f"#{v['idVisitante']} — {v['nombre']} ({v['contacto'] or 'Sin contacto'})": v["idVisitante"]
            for v in visitantes
        }
        excursion_map = {
            (
                f"Parque: {e['nombreParque']} | Área: {e['nombreArea']} | "
                f"Exc #{e['codigoExcursion']} | {e['fecha']} ({e['horario']}) | "
                f"Cupo: {e['inscritosActivos']}/{e['capacidad']}"
            ): (e["numCorrelativo"], e["numInterno"], e["codigoExcursion"])
            for e in excursiones
        }

        with st.form("form_inscripcion_excursion"):
            sel_visitante = st.selectbox("Visitante existente", options=list(visitante_map.keys()))
            sel_excursion = st.selectbox("Excursión existente", options=list(excursion_map.keys()))
            asistencia = st.selectbox("Estado de asistencia", options=list(ESTADOS_ASISTENCIA_VALIDOS), index=0)
            observaciones = st.text_area("Observaciones (opcional)")
            submitted_insc = st.form_submit_button("Registrar inscripción")

        if submitted_insc:
            id_vis = visitante_map[sel_visitante]
            num_corr, num_int, cod_exc = excursion_map[sel_excursion]
            ok, msg = registrar_inscripcion_excursion(
                id_visitante=id_vis,
                num_correlativo=num_corr,
                num_interno=num_int,
                codigo_excursion=cod_exc,
                asistencia=asistencia,
                observaciones=observaciones,
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

    st.markdown("#### Últimas inscripciones registradas")
    st.dataframe(obtener_ultimas_inscripciones(limit=15), use_container_width=True)

with tab_parques:
    st.subheader("Gestión de Parques Naturales (PARQUE_NATURAL)")

    c_busq1, c_busq2 = st.columns([2, 1])
    filtro_p_nombre = c_busq1.text_input("Buscar parque por nombre", key="busq_parque_nombre")
    filtro_p_estado = c_busq2.selectbox(
        "Filtrar por estado de conservación",
        options=["Todos", "Óptimo", "Bueno", "Vulnerable", "En recuperación", "Crítico"],
        key="busq_parque_estado",
    )
    parques = obtener_parques(filtro_texto=filtro_p_nombre, filtro_estado=filtro_p_estado)
    st.dataframe(parques, use_container_width=True)

    st.markdown("#### Crear nuevo parque natural")
    admins_disp = obtener_administradores()
    admin_options = {"Sin asignar": None} | {
        f"#{a['idTrabajador']} — {a['nombre']} ({a['nombreRol'] or 'Sin rol'})": a["idTrabajador"]
        for a in admins_disp
    }

    with st.form("form_crear_parque"):
        p_nombre = st.text_input("Nombre del parque *")
        col_p1, col_p2, col_p3 = st.columns(3)
        p_superficie = col_p1.text_input("Superficie *", value="1200.00")
        p_fecha_decl = col_p2.date_input("Fecha de declaración", value=date(2000, 1, 1))
        p_anio_decl = col_p3.number_input("Año de declaración", min_value=1800, max_value=2200, value=2000)

        col_p4, col_p5, col_p6 = st.columns(3)
        p_estado = col_p4.selectbox("Estado de conservación", options=["Bueno", "Óptimo", "Vulnerable", "En recuperación", "Crítico"])
        p_presupuesto = col_p5.text_input("Presupuesto (opcional)", value="250000.00")
        p_admin_label = col_p6.selectbox("Trabajador administrador (opcional)", options=list(admin_options.keys()))

        submit_crear_parque = st.form_submit_button("Crear parque")

    if submit_crear_parque:
        ok, msg = crear_parque_natural(
            nombre=p_nombre,
            superficie_raw=p_superficie,
            fecha_declaracion=p_fecha_decl,
            anio_declaracion=int(p_anio_decl),
            estado_conservacion=p_estado,
            presupuesto_raw=p_presupuesto,
            id_trabajador_admin=admin_options[p_admin_label],
        )
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    todos_parques = obtener_parques()
    if todos_parques:
        st.markdown("#### Modificar o eliminar parque existente")
        parque_sel_map = {f"#{p['numCorrelativo']} — {p['nombre']}": p for p in todos_parques}
        sel_p_key = st.selectbox("Seleccionar parque", options=list(parque_sel_map.keys()), key="sel_parque_edit")
        parque_actual = parque_sel_map[sel_p_key]

        admins_edit = obtener_administradores(incluir_id_actual=parque_actual["idTrabajadorAdministrador"])
        admin_edit_map = {"Sin asignar": None} | {
            f"#{a['idTrabajador']} — {a['nombre']} ({a['nombreRol'] or 'Sin rol'})": a["idTrabajador"]
            for a in admins_edit
        }
        admin_actual_key = "Sin asignar"
        for k, v in admin_edit_map.items():
            if v == parque_actual["idTrabajadorAdministrador"]:
                admin_actual_key = k
                break

        with st.form("form_editar_parque"):
            e_nombre = st.text_input("Nombre del parque *", value=parque_actual["nombre"])
            col_e1, col_e2, col_e3 = st.columns(3)
            e_superficie = col_e1.text_input("Superficie *", value=str(parque_actual["superficie"]))
            e_fecha_decl = st.date_input("Fecha de declaración", value=parque_actual["fechaDeclaracion"] or date(2000, 1, 1))
            e_anio_decl = col_e3.number_input(
                "Año de declaración",
                min_value=1800,
                max_value=2200,
                value=int(parque_actual["anioDeclaracion"] or 2000),
            )
            col_e4, col_e5, col_e6 = st.columns(3)
            estados_lista = ["Bueno", "Óptimo", "Vulnerable", "En recuperación", "Crítico"]
            idx_estado = estados_lista.index(parque_actual["estadoConservacion"]) if parque_actual["estadoConservacion"] in estados_lista else 0
            e_estado = col_e4.selectbox("Estado de conservación", options=estados_lista, index=idx_estado)
            e_presupuesto = col_e5.text_input(
                "Presupuesto (opcional)",
                value="" if parque_actual["presupuesto"] is None else str(parque_actual["presupuesto"]),
            )
            idx_admin = list(admin_edit_map.keys()).index(admin_actual_key)
            e_admin = col_e6.selectbox("Trabajador administrador", options=list(admin_edit_map.keys()), index=idx_admin)

            c_btn1, c_btn2 = st.columns(2)
            guardar_parque = c_btn1.form_submit_button("Guardar cambios")
            borrar_parque = c_btn2.form_submit_button("Eliminar parque")

        if guardar_parque:
            ok, msg = actualizar_parque_natural(
                num_correlativo=int(parque_actual["numCorrelativo"]),
                nombre=e_nombre,
                superficie_raw=e_superficie,
                fecha_declaracion=e_fecha_decl,
                anio_declaracion=int(e_anio_decl),
                estado_conservacion=e_estado,
                presupuesto_raw=e_presupuesto,
                id_trabajador_admin=admin_edit_map[e_admin],
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

        if borrar_parque:
            ok, msg = eliminar_parque_natural(int(parque_actual["numCorrelativo"]))
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

with tab_especies:
    st.subheader("Gestión de Especies (ESPECIE + VEGETAL / ANIMAL / MINERAL)")

    c_eb1, c_eb2 = st.columns([2, 1])
    filtro_e_texto = c_eb1.text_input("Buscar por denominación científica o nombre vulgar", key="busq_esp_texto")
    filtro_e_tipo = c_eb2.selectbox(
        "Filtrar por especialización",
        options=["Todos", "Sin clasificar", "Vegetal", "Animal", "Mineral"],
        key="busq_esp_tipo",
    )
    especies = obtener_especies(filtro_texto=filtro_e_texto, filtro_tipo=filtro_e_tipo)
    st.dataframe(especies, use_container_width=True)

    st.markdown("#### Crear nueva especie")
    c_tipo_new = st.selectbox("Clasificación / Especialización inicial", options=list(TIPOS_ESPECIE), key="tipo_esp_crear")

    with st.form("form_crear_especie"):
        e_denom = st.text_input("Denominación científica *")
        col_sp1, col_sp2, col_sp3 = st.columns(3)
        e_vulgar = col_sp1.text_input("Nombre vulgar")
        e_est_cons = col_sp2.text_input("Estado de conservación", value="Vulnerable")
        e_fecha_inc = col_sp3.date_input("Fecha de incorporación", value=date.today())

        c_flor = c_alim = c_celo = c_caract = c_rocas = c_crist = None
        if c_tipo_new == "Vegetal":
            c_flor = st.text_input("Floración (VEGETAL)")
        elif c_tipo_new == "Animal":
            c_alim = st.text_input("Alimentación (ANIMAL)")
            c_celo = st.text_input("Período de celo (ANIMAL)")
        elif c_tipo_new == "Mineral":
            c_caract = st.text_area("Características del mineral (MINERAL)")
            c_rocas = st.text_input("Rocas asociadas (MINERAL)")
            c_crist = st.text_input("Cristales (MINERAL)")

        submit_crear_esp = st.form_submit_button("Crear especie")

    if submit_crear_esp:
        ok, msg = crear_especie_catalogo(
            denominacion_cientifica=e_denom,
            nombre_vulgar=e_vulgar,
            estado_conservacion=e_est_cons,
            fecha_incorporacion=e_fecha_inc,
            tipo_especie=c_tipo_new,
            floracion=c_flor,
            alimentacion=c_alim,
            periodo_celo=c_celo,
            caracteristicas_mineral=c_caract,
            rocas=c_rocas,
            cristales=c_crist,
        )
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

    todas_especies = obtener_especies()
    if todas_especies:
        st.markdown("#### Modificar o eliminar especie existente")
        esp_sel_map = {
            f"#{sp['idEspecie']} — {sp['denominacionCientifica']} [{sp['tipoEspecie']}]": sp
            for sp in todas_especies
        }
        sel_sp_key = st.selectbox("Seleccionar especie", options=list(esp_sel_map.keys()), key="sel_esp_edit")
        esp_actual = esp_sel_map[sel_sp_key]

        idx_tipo_actual = list(TIPOS_ESPECIE).index(esp_actual["tipoEspecie"]) if esp_actual["tipoEspecie"] in TIPOS_ESPECIE else 0
        tipo_edit = st.selectbox(
            "Clasificación / Especialización",
            options=list(TIPOS_ESPECIE),
            index=idx_tipo_actual,
            key="tipo_esp_editar",
        )

        with st.form("form_editar_especie"):
            ed_denom = st.text_input("Denominación científica *", value=esp_actual["denominacionCientifica"])
            col_ed1, col_ed2, col_ed3 = st.columns(3)
            ed_vulgar = col_ed1.text_input("Nombre vulgar", value=esp_actual["nombreVulgar"] or "")
            ed_est_cons = col_ed2.text_input("Estado de conservación", value=esp_actual["estadoConservacion"] or "")
            ed_fecha_inc = st.date_input(
                "Fecha de incorporación",
                value=esp_actual["fechaIncorporacion"] or date.today(),
            )

            ed_flor = ed_alim = ed_celo = ed_caract = ed_rocas = ed_crist = None
            if tipo_edit == "Vegetal":
                ed_flor = st.text_input("Floración (VEGETAL)", value=esp_actual["floracion"] or "")
            elif tipo_edit == "Animal":
                ed_alim = st.text_input("Alimentación (ANIMAL)", value=esp_actual["alimentacion"] or "")
                ed_celo = st.text_input("Período de celo (ANIMAL)", value=esp_actual["periodoCelo"] or "")
            elif tipo_edit == "Mineral":
                ed_caract = st.text_area("Características del mineral (MINERAL)", value=esp_actual["caracteristicasMineral"] or "")
                ed_rocas = st.text_input("Rocas asociadas (MINERAL)", value=esp_actual["rocas"] or "")
                ed_crist = st.text_input("Cristales (MINERAL)", value=esp_actual["cristales"] or "")

            eb1, eb2 = st.columns(2)
            guardar_esp = eb1.form_submit_button("Guardar cambios de especie")
            borrar_esp = eb2.form_submit_button("Eliminar especie")

        if guardar_esp:
            ok, msg = actualizar_especie_catalogo(
                id_especie=int(esp_actual["idEspecie"]),
                denominacion_cientifica=ed_denom,
                nombre_vulgar=ed_vulgar,
                estado_conservacion=ed_est_cons,
                fecha_incorporacion=ed_fecha_inc,
                tipo_especie=tipo_edit,
                floracion=ed_flor,
                alimentacion=ed_alim,
                periodo_celo=ed_celo,
                caracteristicas_mineral=ed_caract,
                rocas=ed_rocas,
                cristales=ed_crist,
            )
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)

        if borrar_esp:
            ok, msg = eliminar_especie_catalogo(int(esp_actual["idEspecie"]))
            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
