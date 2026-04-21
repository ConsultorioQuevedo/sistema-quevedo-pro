import streamlit as st
import pandas as pd
import webbrowser

def mostrar_asistente(conn, c):
    st.header("🤖 ASISTENTE DE QUEVEDO")
    st.divider()

    try:
        df = pd.read_sql_query("SELECT fecha, glucosa, presion FROM salud ORDER BY id DESC LIMIT 1", conn)
        
        if not df.empty:
            glu = df['glucosa'].iloc[0]
            pre = df['presion'].iloc[0]
            
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Última Glucosa", f"{glu} mg/dL")
                if glu > 140: st.error("Nivel Alto")
                elif glu < 70: st.warning("Nivel Bajo")
                else: st.success("Nivel Normal")
            with c2:
                st.metric("Última Presión", pre)
        else:
            st.info("Esperando datos para analizar...")
    except:
        st.error("No se pudo leer la base de datos.")

    st.divider()
    st.subheader("📲 Comunicación Rápida")
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if st.button("💬 WhatsApp GBC"): webbrowser.open_new_tab("https://web.whatsapp.com/")
    with btn2:
        if st.button("💬 WhatsApp Valued"): webbrowser.open_new_tab("https://web.whatsapp.com/")
    with btn3:
        if st.button("📧 Abrir Gmail"): webbrowser.open_new_tab("https://mail.google.com/")
                  
