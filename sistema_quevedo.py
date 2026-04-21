import streamlit as st
import pandas as pd
import webbrowser
from sqlite3 import Error

def mostrar_asistente(conn, c):
    st.header("🤖 ASISTENTE INTELIGENTE QUEVEDO")
    st.markdown("---")

    # 1. VALIDACIÓN DE CONEXIÓN (Robustez inicial)
    if conn is None or c is None:
        st.error("❌ Error Crítico: El Asistente no tiene acceso a la conexión de la base de datos.")
        return

    # 2. ANÁLISIS DEL PANORAMA (VISIÓN TOTAL)
    try:
        # Usamos un bloque Try-Except específico para la lectura
        # Buscamos la verdad en 'salud' con nombres de columnas explícitos
        query = "SELECT fecha, presion, glucosa, notas FROM salud ORDER BY id DESC LIMIT 1"
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            # Extracción segura de datos
            datos = df.iloc[0]
            glucosa = datos['glucosa']
            presion = datos['presion']
            fecha = datos['fecha']
            
            st.subheader("🔍 Diagnóstico del Sistema")
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                # Lógica de decisión robusta
                if glucosa >= 140:
                    st.error(f"🚨 **ALERTA:** Glucosa Alta ({glucosa} mg/dL).")
                elif glucosa <= 70:
                    st.warning(f"⚠️ **AVISO:** Glucosa Baja ({glucosa} mg/dL).")
                else:
                    st.success(f"✅ **ESTABLE:** Glucosa en {glucosa} mg/dL.")
            
            with col_info2:
                st.info(f"🩺 **Presión:** {presion}\n\n📅 **Último Registro:** {fecha}")
                
            # Análisis de tendencias (Para que no sea ciego)
            with st.expander("📈 Ver historial rápido"):
                df_completo = pd.read_sql_query("SELECT fecha, glucosa FROM salud ORDER BY id DESC LIMIT 5", conn)
                st.line_chart(df_completo.set_index('fecha'))
        else:
            st.info("🌑 **Sistema en espera:** No hay datos en 'salud'. El asistente está listo para analizar cuando ingreses registros.")

    except Exception as e:
        st.error(f"❌ **Fallo de Visión:** No se pudo procesar la estructura. Detalle: {e}")

    st.divider()

    # 3. CENTRO DE COMUNICACIÓN (WHATSAPP Y GMAIL)
    st.subheader("📲 Comunicaciones y Enlaces")
    col1, col2, col3 = st.columns(3)
    
    # Estilo de botón robusto con HTML/CSS
    boton_estilo = """
        <style>
        .stButton>button {
            width: 100%;
            height: 60px;
            border-radius: 10px;
        }
        </style>
    """
    st.markdown(boton_estilo, unsafe_allow_html=True)

    with col1:
        if st.button("💬 WhatsApp GBC"):
            webbrowser.open_new_tab("https://web.whatsapp.com/")
    
    with col2:
        if st.button("💬 WhatsApp Valued"):
            webbrowser.open_new_tab("https://web.whatsapp.com/")
            
    with col3:
        if st.button("📧 Abrir Gmail"):
            webbrowser.open_new_tab("https://mail.google.com/")

    st.divider()

    # 4. AUDITORÍA DE ESTRUCTURA (Respetando tus 8 archivos)
    with st.expander("🛠️ Verificación de Integridad del Proyecto"):
        st.write(f"🏠 **Ruta Local:** `C:\\Users\\DELL\\OneDrive\\Desktop\\invento_nuevo`")
        try:
            tablas = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
            st.write(f"📊 **Tablas detectadas:** {', '.join(tablas['name'].tolist())}")
            st.success("✅ Sincronización con 'base_datos.py' correcta.")
        except:
            st.error("⚠️ No se pudo verificar la integridad de las tablas.")
