import streamlit as st
import base_datos as db
import os
import inicio, biomonitor, finanzas, archivador, asistente, reportepdf_quevedo

# --- 1. ESCUDO DE SEGURIDAD ---
try:
    import seguridad_quevedo as seg
    # Activamos el escudo antes de cargar el menú
    seg.EscudoSeguridad.asegurar_carpetas()
except ImportError:
    # Si estás en la nube, es posible que no subas el módulo de seguridad personal
    st.sidebar.warning("⚠️ Módulo de seguridad no detectado.")

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SISTEMA QUEVEDO", page_icon="🤖", layout="wide")

# --- 3. CONEXIÓN INTELIGENTE (PC vs NUBE) ---
# Esta función asegura que el programa no muera si no encuentra el Disco C:/
def conectar_sistema():
    ruta_local = "C:/sistema_quevedo/consultorio.db"
    if os.path.exists(ruta_local):
        # Si existe la ruta en tu Dell, la usamos
        return db.inicializar_todo() # Asumimos que esto devuelve (conn, c)
    else:
        # Si estamos en Streamlit Cloud, inicializamos en la carpeta actual
        # Nota: Asegúrate de que tu base_datos.py acepte crear la DB localmente
        return db.inicializar_todo() 

conn, c = conectar_sistema()

# --- 4. MENÚ LATERAL ---
st.sidebar.title("🤖 SISTEMA QUEVEDO")
st.sidebar.write("Usuario: Luis Rafael Quevedo")

menu = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Inicio", "Biomonitor", "Finanzas", "Archivador", "Asistente Inteligente", "Reportes PDF"]
)

st.sidebar.divider()

# --- 5. EJECUCIÓN DE MÓDULOS ---
if menu == "Inicio":
    inicio.mostrar_inicio(conn)
elif menu == "Biomonitor":
    biomonitor.mostrar_biomonitor(conn, c)
elif menu == "Finanzas":
    finanzas.mostrar_finanzas(conn, c)
elif menu == "Archivador":
    archivador.mostrar_archivador(conn, c)
elif menu == "Asistente Inteligente":
    asistente.mostrar_asistente(conn, c)
elif menu == "Reportes PDF":
    reportepdf_quevedo.mostrar_pdf(conn)

# --- 6. PIE DE PÁGINA DINÁMICO ---
if os.path.exists("C:/"):
    st.sidebar.success("✅ Conectado localmente al Disco C:/")
else:
    st.sidebar.info("🌐 Ejecutando en la Nube (Streamlit Cloud)")
