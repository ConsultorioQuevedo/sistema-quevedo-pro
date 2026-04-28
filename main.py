import streamlit as st
import base_datos as db
import os
import inicio, biomonitor, finanzas, archivador, asistente, reportepdf_quevedo

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="SISTEMA QUEVEDO", page_icon="icono.ico", layout="wide")

# --- CONEXIÓN ---
conn, c = db.inicializar_todo()

# --- MENÚ LATERAL ---
# Inserción del logo sobre el título del menú
st.sidebar.image("logo.png", use_container_width=True)

st.sidebar.title("🤖 SISTEMA QUEVEDO")
st.sidebar.write("Usuario: Luis Rafael Quevedo")

menu = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Inicio", "Biomonitor", "Finanzas", "Archivador", "Asistente Inteligente", "Reportes PDF"]
)

# --- NAVEGACIÓN SINCRONIZADA ---
if menu == "Inicio":
    # Aquí es donde se activa tu diseño, el Log y la Neurona
    inicio.mostrar_inicio(conn)

elif menu == "Biomonitor":
    biomonitor.mostrar_biomonitor(conn, c)

elif menu == "Finanzas":
    finanzas.mostrar_finanzas(conn, c)

elif menu == "Archivador":
    archivador.mostrar_archivador(conn, c)

elif menu == "Asistente Inteligente":
    # Le pasamos la conexión para que el cerebro de la IA funcione
    asistente.mostrar_asistente(conn, c)

elif menu == "Reportes PDF":
    reportepdf_quevedo.mostrar_pdf(conn)

st.sidebar.markdown("---")
st.sidebar.info("Sistema Quevedo Pro v2.0 - Activo")
