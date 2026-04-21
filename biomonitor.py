import streamlit as st
import pandas as pd
from datetime import datetime
import base_datos as db
import logger_quevedo as log
import seguridad_quevedo as seg

def mostrar_biomonitor(conn, c):
    # 0. SEGURIDAD SILENCIOSA
    seg.EscudoSeguridad.asegurar_carpetas()

    # TÍTULO E INTERFAZ (Tu diseño original)
    st.markdown("<h1 style='text-align: center; color: #01579b;'>🩺 CONTROL DE BIOMETRÍA</h1>", unsafe_allow_html=True)
    st.divider()

    # 1. FORMULARIO DE ENTRADA
    st.subheader("📝 Registrar Nuevos Valores")
    with st.form("form_salud", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            presion = st.text_input("Presión Arterial (ej: 120/80)")
            glucosa = st.number_input("Glucosa (mg/dL)", min_value=0, step=1)
        with col2:
            notas = st.text_area("Notas adicionales o síntomas", height=108)
        
        boton_guardar = st.form_submit_button("🚀 Guardar en Historial")

    # LÓGICA DE GUARDADO
    if boton_guardar:
        if presion and glucosa > 0:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # Inserción en la base de datos del Disco C
                c.execute("INSERT INTO salud (fecha, presion, glucosa, notas) VALUES (?, ?, ?, ?)",
                          (fecha_actual, presion, glucosa, notas))
                conn.commit()
                
                # REGISTRO EN LA CAJA NEGRA (LOG)
                log.registrar(f"REGISTRO SALUD: Glucosa {glucosa}, Presión {presion}")
                
                st.success("✅ Registro guardado en el Disco C")
                st.rerun() 
            except Exception as e:
                log.registrar(f"ERROR GUARDADO SALUD: {e}")
                st.error(f"Error técnico al guardar: {e}")
        else:
            st.warning("Por favor, completa los campos de Presión y Glucosa.")

    st.divider()

    # 2. HISTORIAL VISUAL Y BORRADO (Tu diseño de expansores)
    st.subheader("📋 Historial de Registros")
    try:
        df = pd.read_sql_query("SELECT * FROM salud ORDER BY id DESC", conn)

        if not df.empty:
            # ANÁLISIS AUTOMÁTICO (Un extra para Luis)
            ultima_g = df['glucosa'].iloc[0]
            if ultima_g > 140:
                st.warning(f"⚠️ Atención: Tu último registro de glucosa ({ultima_g}) está elevado.")
            elif 0 < ultima_g < 70:
                st.info(f"ℹ️ Aviso: Tu glucosa ({ultima_g}) está baja.")

            # Bucle de registros
            for index, row in df.iterrows():
                with st.expander(f"📅 Registro: {row['fecha']} | Glucosa: {row['glucosa']}"):
                    col_data, col_action = st.columns([4, 1])
                    
                    with col_data:
                        st.write(f"**Presión Arterial:** {row['presion']}")
                        if row['notas']:
                            st.info(f"**Nota:** {row['notas']}")
                    
                    with col_action:
                        # BOTÓN DE BORRADO INTELIGENTE
                        if st.button("🗑️ Borrar", key=f"del_{row['id']}"):
                            if db.eliminar_registro("salud", row['id']):
                                log.registrar(f"REGISTRO ELIMINADO: ID {row['id']}")
                                st.error(f"Registro {row['id']} eliminado")
                                st.rerun()
        else:
            st.info("No hay datos registrados en el Biomonitor.")
            
    except Exception as e:
        log.registrar(f"ERROR CARGA BIOMONITOR: {e}")
        st.error(f"Error al cargar el historial: {e}")
