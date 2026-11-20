import streamlit as st
from db.connection import wait_for_database
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
    st.error("No se pudo conectar o consultar MySQL. Verifica que el contenedor db esté activo y que las variables de entorno coincidan.")
    st.info("La aplicación reintenta la conexión durante un período limitado al iniciar.")
    st.exception(exc)
