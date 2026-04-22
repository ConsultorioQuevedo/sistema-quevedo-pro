import streamlit as st
import google.generativeai as genai

def consultar_neurona(pregunta):
    # Trae la llave desde los Secrets o el config
    api_key = st.secrets.get("API_KEY_QUEVEDO")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        # Aquí sucede la magia
        respuesta = model.generate_content(pregunta)
        return respuesta.text
    else:
        return "Error: La neurona no tiene energía (Falta API Key)."
