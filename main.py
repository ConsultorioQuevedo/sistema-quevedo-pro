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
    # Ahora db.inicializar_todo() existe sí o sí
    return db.inicializar_todo() 

conn, c = conectar_sistema()

# --- 4. MENÚ LATERAL ---
st.sidebar.title("🤖 SISTEMA QUEVEDO")
st.sidebar.write("Usuario: Luis Rafael Quevedo")

menu = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Inicio", "Biomonitor", "Finanzas", "Archivador", "Asistente Inteligente", "Reportes PDF"]
)

# --- 5. LÓGICA DE NAVEGACIÓN ---
if menu == "Inicio":
    inicio.mostrar_inicio()
elif menu == "Biomonitor":
    biomonitor.mostrar_biomonitor()
elif menu == "Finanzas":
    finanzas.mostrar_finanzas()
elif menu == "Archivador":
    archivador.mostrar_archivador()
elif menu == "Asistente Inteligente":
    asistente.mostrar_asistente()
elif menu == "Reportes PDF":
    reportepdf_quevedo.mostrar_reportes()

# --- 6. PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.info("Sistema Quevedo Pro v2.0 - Activo")
