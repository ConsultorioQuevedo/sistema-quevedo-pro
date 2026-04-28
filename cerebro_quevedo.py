import google.generativeai as genai
import pandas as pd
import streamlit as st

def conectar_neurona():
    try:
        # Usamos la llave guardada en los Secretos de Streamlit para mayor seguridad
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Usamos el modelo 1.5 Flash que es el más rápido y estable actualmente
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Error al conectar con la neurona: {e}")
        return None

# Inicializamos la neurona una sola vez
if "model_ia" not in st.session_state:
    st.session_state.model_ia = conectar_neurona()

def obtener_analisis_ia(conn):
    try:
        df_f = pd.read_sql_query("SELECT monto, descripcion FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        datos = df_f.to_dict('records') if not df_f.empty else "Sin movimientos"
        
        model = st.session_state.model_ia
        if model:
            prompt = f"Luis Quevedo, experto en tecnología. Analiza mis últimos movimientos financieros: {datos}. Dame un consejo motivador y profesional muy corto."
            response = model.generate_content(prompt)
            return response.text
        return "La neurona está esperando órdenes."
    except Exception as e:
        return f"Error en análisis: {str(e)}"

def procesar_consulta_asistente(consulta, conn):
    model = st.session_state.model_ia
    if not model: 
        st.session_state.model_ia = conectar_neurona()
        model = st.session_state.model_ia
    
    try:
        if model:
            # Instrucción de identidad para que Gemini siempre sepa a quién le responde
            instruccion = f"Responde como la Neurona del Sistema Quevedo a Luis Rafael Quevedo. Consulta: {consulta}"
            response = model.generate_content(instruccion)
            return response.text
        return "No se pudo establecer conexión con las neuronas de Gemini."
    except Exception as e:
        return f"Error en el chat: {str(e)}"
