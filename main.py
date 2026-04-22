import streamlit as st
import base_datos as db
import os
import inicio, biomonitor, finanzas, archivador, asistente, reportepdf_quevedo

# --- 1. ESCUDO DE SEGURIDAD ---
try:
    import seguridad_quevedo as seg
    seg.EscudoSeguridad.asegurar_carpetas()
except (ImportError, AttributeError):
    st.sidebar.warning("⚠️ Módulo de seguridad en modo local.")

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SISTEMA QUEVEDO", page_icon="🤖", layout="wide")

# --- 3. CONEXIÓN INTELIGENTE ---
def conectar_sistema():
    # Esta función debe devolver la conexión y el cursor
    return db.inicializar_todo() 

# Aquí guardamos los "cables" de la base de datos
conn, c = conectar_sistema()

# --- 4. MENÚ LATERAL ---
st.sidebar.title("🤖 SISTEMA QUEVEDO")
st.sidebar.write("Usuario: Luis Rafael Quevedo")

menu = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Inicio", "Biomonitor", "Finanzas", "Archivador", "Asistente Inteligente", "Reportes PDF"]
)

# --- 5. LÓGICA DE NAVEGACIÓN (CORREGIDA LÍNEA POR LÍNEA) ---
if menu == "Inicio":
    inicio.mostrar_inicio()

elif menu == "Biomonitor":
    # Le pasamos conn y c para que pueda guardar datos
    biomonitor.mostrar_biomonitor(conn, c)

elif menu == "Finanzas":
    # Le pasamos conn y c para sus tablas financieras
    finanzas.mostrar_finanzas(conn, c)

elif menu == "Archivador":
    # Le pasamos conn y c para gestionar archivos
    archivador.mostrar_archivador(conn, c)

elif menu == "Asistente Inteligente":
    asistente.mostrar_asistente()

elif menu == "Reportes PDF":
    # Le pasamos conn y c para generar el PDF con datos reales
    reportepdf_quevedo.mostrar_reportes(conn, c)

# --- 6. PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.info("Sistema Quevedo Pro v2.0 - Activo")
