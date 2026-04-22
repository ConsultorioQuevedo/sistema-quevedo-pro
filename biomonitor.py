import streamlit as st
import pandas as pd
from datetime import datetime
import base_datos as db
import logger_quevedo as log
import seguridad_quevedo as seg

def mostrar_biomonitor(conn, c):
    # 0. SEGURIDAD
    try:
        seg.EscudoSeguridad.asegurar_carpetas()
    except:
        pass

    st.markdown("<h1 style='text-align: center; color: #01579b;'>🩺 CONTROL DE BIOMETRÍA</h1>", unsafe_allow_html=True)
    st.divider()

    # 1. FORMULARIO
    st.subheader("📝 Registrar Nuevos Valores")
    with st.form("form_salud", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            presion = st.text_input("Presión Arterial (ej: 120/80)")
            glucosa = st.number_input("Glucosa (mg/dL)", min_value=0, step=1)
        with col2:
            notas = st.text_area("Notas adicionales o síntomas", height=108)
        
        boton_guardar = st.form_submit_button("🚀 Guardar en Historial")

    if boton_guardar:
        if presion and glucosa > 0:
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                # Ahora los nombres coinciden con base_datos.py
                c.execute("INSERT INTO salud (fecha, presion, glucosa, notas) VALUES (?, ?, ?, ?)",
                          (fecha_actual, presion, glucosa, notas))
                conn.commit()
                st.success("✅ Registro guardado")
                st.rerun() 
            except Exception as e:
                st.error(f"Error técnico al guardar: {e}")
        else:
            st.warning("Por favor, completa los campos.")

    st.divider()

    # 2. HISTORIAL
    st.subheader("📋 Historial de Registros")
    try:
        df = pd.read_sql_query("SELECT * FROM salud ORDER BY id DESC", conn)
        if not df.empty:
            for index, row in df.iterrows():
                with st.expander(f"📅 {row['fecha']} | Glucosa: {row['glucosa']}"):
                    col_data, col_action = st.columns([4, 1])
                    with col_data:
                        st.write(f"**Presión:** {row['presion']}")
                        if row['notas']: st.info(f"**Nota:** {row['notas']}")
                    with col_action:
                        if st.button("🗑️ Borrar", key=f"del_{row['id']}"):
                            if db.eliminar_registro("salud", row['id']):
                                st.rerun()
        else:
            st.info("No hay datos registrados.")
    except Exception as e:
        st.error(f"Error al cargar historial: {e}")
