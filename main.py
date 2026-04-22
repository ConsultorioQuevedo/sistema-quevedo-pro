import streamlit as st
import base_datos as db
import os
import inicio, biomonitor, finanzas, archivador, asistente, reportepdf_quevedo

# --- 1. ESCUDO DE SEGURIDAD ---
try:
    import seguridad_quevedo as seg
    # Activamos el escudo antes de cargar el menú
    seg.EscudoSeguridad.asegurar_carpetas()
except (ImportError, AttributeError):
    # Si estás en la nube, es posible que no subas el módulo de seguridad personal
    st.sidebar.warning("⚠️ Módulo de seguridad no detectado.")

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SISTEMA QUEVEDO", page_icon="🤖", layout="wide")

# --- 3. CONEXIÓN INTELIGENTE (PC vs NUBE) ---
# Esta función asegura que el programa no muera si no encuentra el Disco C:/
def conectar_sistema():
    # Nota: Tu base_datos.py ya tiene la lógica de DB_PATH en C:/
    # Aquí simplemente llamamos a inicializar para asegurar que las tablas existan
    return db.inicializar_todo() 

conn, c = conectar_sistema()

# --- 4. MENÚ LATERAL ---
st.sidebar.title("🤖 SISTEMA QUEVEDO")
st.sidebar.write("Usuario: Luis Rafael Quevedo")

menu = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Inicio", "Biomonitor", "Finanzas", "Archivador", "Asistente Inteligente", "Reportes PDF"]
)

# --- 5. LOGICA DE NAVEGACIÓN (CONTROL DE MÓDULOS) ---
# Aquí es donde la artillería se despliega según tu selección
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
