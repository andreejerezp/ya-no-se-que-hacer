import streamlit as st
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db.connection import wait_for_database
from db import pmv_dao
from services.metrics_service import get_home_metrics
from services.inscripcion_service import register_visitor, visitor_options, excursion_options
from services.species_service import search_species, add_species, edit_species, remove_species
from services.park_service import search_parks, add_park, edit_park, remove_park

st.set_page_config(page_title="Parques Naturales", page_icon="🌿", layout="wide")
st.markdown("""\n<style>utton[kind="primary"] {background:#96333B;color:white;border:0;border-radius:8px;}
button[kind="primary"]:hover {background:#7A2730;color:white;}
</style>
""", unsafe_allow_html=True)
st.title("🌿 Sistema Integral de Gestión de Parques Naturales")
st.write("Aplicación inicial del PMV — Caso 1, Fase 2.")
st.caption("Conexión real a MySQL mediante SQLAlchemy + PyMySQL.")

try:
    wait_for_database()
    metrics = get_home_metrics()
    c1, c2 = st.columns(2)
    c1.metric("Visitantes registrados", metrics["visitantes"])
    c2.metric("Excursiones registradas", metrics["excursiones"])
    st.success("Conexión a MySQL exitosa y consultas ejecutadas.")
except Exception as exc:
    st.error("No se pudo conectar o consultar MySQL. Verifica que el contenedor db esté activo y las variables de entorno coincidan.")
    st.exception(exc)
    st.stop()

home, inscription_tab, species_tab, parks_tab = st.tabs(["Inicio", "Inscripción a excursión", "Gestión de especies", "Gestión de parques"])
with home:
    st.info("Las métricas originales del Video 6 se mantienen. Usa las pestañas para realizar las operaciones del Video 7.")


with inscription_tab:
    st.subheader("Registrar visitante en una excursión")
    visitors = visitor_options()
    excursions = excursion_options()
    if not visitors:
        st.warning("No hay visitantes registrados. Primero debe existir al menos un visitante.")
    elif not excursions:
        st.warning("No hay excursiones registradas. Primero debe existir una excursión.")
    else:
        visitor_labels = {f"{v['nombre']} (ID {v['idVisitante']})": v["idVisitante"] for v in visitors}
        excursion_labels = {}
        for e in excursions:
            label = (f"{e['parque']} / {e['area']} — {e['modalidad']} | {e['fecha']} | "
                     f"Exc. {e['codigoExcursion']} (cap. {e['capacidad']})")
            excursion_labels[label] = (e["numCorrelativo"], e["numInterno"], e["codigoExcursion"])
        with st.form("form_inscripcion", clear_on_submit=True):
            visitor_label = st.selectbox("Visitante", list(visitor_labels.keys()))
            excursion_label = st.selectbox("Excursión", list(excursion_labels.keys()))
            observations = st.text_area("Observaciones (opcional)")
            submitted = st.form_submit_button("Registrar inscripción", type="primary")
        if submitted:
            try:
                register_visitor(excursion_labels[excursion_label], visitor_labels[visitor_label], observations)
                st.success("Inscripción registrada correctamente.")
                st.rerun()
            except ValueError as exc:
                st.warning(str(exc))
            except IntegrityError:
                st.error("No se pudo registrar: posible inscripción duplicada o clave foránea inválida.")
            except SQLAlchemyError as exc:
                st.error("Error de base de datos. La transacción fue revertida.")
                st.exception(exc)

with species_tab:
    st.subheader("Crear especie")
    with st.form("form_especie", clear_on_submit=True):
        common_name = st.text_input("Nombre vulgar")
        scientific_name = st.text_input("Denominación científica *")
        conservation = st.text_input("Estado de conservación")
        date_added = st.date_input("Fecha de incorporación")
        subtype = st.selectbox("Subtipo (especialización parcial)", ["Sin subtipo", "Vegetal", "Animal", "Mineral"])
        d1 = d2 = d3 = None
        if subtype == "Vegetal":
            d1 = st.text_input("Floración")
        elif subtype == "Animal":
            d1 = st.text_input("Alimentación")
            d2 = st.text_input("Período de celo")
        elif subtype == "Mineral":
            d1 = st.text_area("Características mineral")
            d2 = st.text_input("Rocas")
            d3 = st.text_input("Cristales")
        create_submitted = st.form_submit_button("Crear especie", type="primary")
    if create_submitted:
        try:
            add_species(common_name, scientific_name, conservation, date_added, subtype, d1, d2, d3)
            st.success("Especie creada.")
            st.rerun()
        except IntegrityError:
            st.error("La denominación científica ya existe o hay un conflicto de integridad.")
        except (ValueError, SQLAlchemyError) as exc:
            st.error(f"No se pudo crear la especie: {exc}")

    st.divider()
    st.subheader("Consultar / modificar / eliminar especies")
    term = st.text_input("Buscar por nombre vulgar o científico", key="species_search")
    species = search_species(term)
    st.dataframe([dict(s) for s in species], use_container_width=True, hide_index=True)
    if species:
        options = {f"{s['denominacionCientifica']} (ID {s['idEspecie']})": s for s in species}
        selected_label = st.selectbox("Especie a modificar/eliminar", list(options.keys()), key="species_selected")
        selected = options[selected_label]
        with st.form("edit_species"):
            new_common = st.text_input("Nombre vulgar", value=selected["nombreVulgar"] or "")
            new_scientific = st.text_input("Denominación científica", value=selected["denominacionCientifica"])
            new_conservation = st.text_input("Estado de conservación", value=selected["estadoConservacion"] or "")
            new_date = st.date_input("Fecha de incorporación", value=selected["fechaIncorporacion"] or __import__('datetime').date.today())
            update_clicked = st.form_submit_button("Guardar cambios", type="primary")
        if update_clicked:
            try:
                edit_species(selected["idEspecie"], new_common, new_scientific, new_conservation, new_date)
                st.success("Especie actualizada.")
                st.rerun()
            except IntegrityError:
                st.error("La denominación científica ya está utilizada.")
            except (ValueError, SQLAlchemyError) as exc:
                st.error(f"No se pudo modificar: {exc}")
        if st.button("Eliminar especie seleccionada", key="delete_species"):
            try:
                remove_species(selected["idEspecie"])
                st.success("Especie eliminada.")
                st.rerun()
            except IntegrityError:
                st.error("No se puede eliminar: esta especie está referenciada en inventarios o proyectos de investigación.")
            except SQLAlchemyError as exc:
                st.error(f"Error al eliminar: {exc}")

with parks_tab:
    st.subheader("Crear parque natural")
    with st.form("form_park", clear_on_submit=True):
        park_name = st.text_input("Nombre del parque *")
        surface = st.number_input("Superficie", min_value=0.01, value=1.0, step=1.0)
        declaration_date = st.date_input("Fecha de declaración")
        year = st.number_input("Año de declaración (opcional)", min_value=1800, max_value=2200, value=2020)
        park_conservation = st.text_input("Estado de conservación")
        budget = st.number_input("Presupuesto (0 si no se informa)", min_value=0.0, value=0.0, step=1000.0)
        park_admin = st.number_input("ID trabajador administrador (opcional; 0 = sin asignar)", min_value=0, value=0, step=1)
        create_park_clicked = st.form_submit_button("Crear parque", type="primary")
    if create_park_clicked:
        try:
            add_park(park_name, surface, declaration_date, int(year) if year else None,
                     park_conservation, budget if budget > 0 else None, park_admin or None)
            st.success("Parque creado.")
            st.rerun()
        except IntegrityError:
            st.error("Nombre duplicado o ID de administrador inexistente.")
        except (ValueError, SQLAlchemyError) as exc:
            st.error(f"No se pudo crear el parque: {exc}")

    st.divider()
    st.subheader("Consultar / modificar / eliminar parques")
    park_term = st.text_input("Buscar parque por nombre", key="park_search")
    parks = search_parks(park_term)
    st.dataframe([dict(p) for p in parks], use_container_width=True, hide_index=True)
    if parks:
        park_options = {f"{p['nombre']} (ID {p['numCorrelativo']})": p for p in parks}
        park_label = st.selectbox("Parque a modificar/eliminar", list(park_options.keys()), key="park_selected")
        park = park_options[park_label]
        with st.form("edit_park"):
            edit_name = st.text_input("Nombre", value=park["nombre"])
            edit_surface = st.number_input("Superficie", min_value=0.01, value=float(park["superficie"]), step=1.0)
            edit_date = st.date_input("Fecha de declaración", value=park["fechaDeclaracion"] or __import__('datetime').date.today())
            edit_year = st.number_input("Año", min_value=1800, max_value=2200, value=int(park["anioDeclaracion"] or 2020))
            edit_conservation = st.text_input("Estado de conservación", value=park["estadoConservacion"] or "")
            edit_budget = st.number_input("Presupuesto", min_value=0.0, value=float(park["presupuesto"] or 0.0), step=1000.0)
            edit_admin = st.number_input("ID administrador (0 = sin asignar)", min_value=0, value=int(park["idTrabajadorAdministrador"] or 0), step=1)
            save_park = st.form_submit_button("Guardar cambios", type="primary")
        if save_park:
            try:
                edit_park(park["numCorrelativo"], edit_name, edit_surface, edit_date,
                         int(edit_year) if edit_year else None, edit_conservation,
                         edit_budget if edit_budget > 0 else None, edit_admin or None)
                st.success("Parque actualizado.")
                st.rerun()
            except IntegrityError:
                st.error("Nombre duplicado o administrador inexistente.")
            except (ValueError, SQLAlchemyError) as exc:
                st.error(f"No se pudo actualizar: {exc}")
        if st.button("Eliminar parque seleccionado", key="delete_park"):
            try:
                remove_park(park["numCorrelativo"])
                st.success("Parque eliminado.")
                st.rerun()
            except IntegrityError:
                st.error("No se puede eliminar: el parque tiene áreas, trabajadores, proyectos u otras relaciones.")
            except SQLAlchemyError as exc:
                st.error(f"Error al eliminar: {exc}")
