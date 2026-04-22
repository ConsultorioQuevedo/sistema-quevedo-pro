import streamlit as st
import google.generativeai as genai

def consultar_neurona(pregunta):
    """
    Activa la neurona especialista con configuración de seguridad 
    y perfil médico de alto nivel.
    """
    # 1. BÚSQUEDA INTELIGENTE DE LA API KEY (Nube o Local)
    # Primero intenta leer desde los Secrets de Streamlit (Nube)
    api_key = st.secrets.get("API_KEY_QUEVEDO")
    
    # Si no la encuentra (estás en tu PC), intenta leerla de config.py
    if not api_key:
        try:
            import config
            api_key = config.API_KEY_QUEVEDO
        except (ImportError, AttributeError):
            api_key = None

    # 2. VALIDACIÓN Y ACTIVACIÓN
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # DEFINICIÓN DEL PERFIL ESPECIALISTA (SYSTEM INSTRUCTION)
            instrucciones_medicas = (
                "Actúa como el Director Médico Jefe del Consultorio Quevedo. "
                "Eres un experto en medicina interna y análisis de biomonitoreo. "
                "Tus respuestas deben ser precisas, profesionales y enfocadas en "
                "la prevención y salud del paciente."
            )

            # Configuración del modelo Gemini 1.5 Flash
            model = genai.GenerativeModel(
                model_name='gemini-1.5-flash',
                system_instruction=instrucciones_medicas
            )
            
            # 3. GENERACIÓN DE RESPUESTA
            respuesta = model.generate_content(pregunta)
            return respuesta.text

        except Exception as e:
            return f"⚠️ Error técnico en la neurona: {str(e)}"
    else:
        # Mensaje de error si no hay combustible (API KEY)
        return "❌ Error: La neurona no tiene energía (Falta API Key en Secrets o config.py)."
