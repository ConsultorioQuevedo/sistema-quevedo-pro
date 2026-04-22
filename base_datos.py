import streamlit as st
import google.generativeai as genai

def consultar_neurona(pregunta):
    """
    Activa la neurona especialista con configuración de seguridad 
    y perfil médico de alto nivel.
    """
    # 1. Búsqueda inteligente de la API KEY (Nube o Local)
    api_key = st.secrets.get("API_KEY_QUEVEDO")
    
    if not api_key:
        try:
            import config
            api_key = config.API_KEY_QUEVEDO
        except (ImportError, AttributeError):
            api_key = None

    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # 2. DEFINICIÓN DEL ESPECIALISTA (SYSTEM INSTRUCTION)
            # Esto es lo que hace grande a la neurona
            instrucciones_medicas = (
                "Actúa como el Director Médico Jefe del Consultorio Quevedo. "
                "Eres un experto en medicina interna y análisis de biomonitoreo. "
                "Tus respuestas deben ser precisas, profesionales y enfocadas en "
                "la prevención y salud del paciente."
            )

            # Usamos gemini-1.5-flash para mayor velocidad y escala
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=instrucciones_medicas
            )
            
            # 3. GENERACIÓN DE CONTENIDO
            respuesta = model.generate_content(pregunta)
            return respuesta.text

        except Exception as e:
            return f"⚠️ Error técnico en la neurona: {str(e)}"
    else:
        return "❌ Error: La neurona no tiene energía (Falta API Key en Secrets o config.py)."
