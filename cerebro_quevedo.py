import streamlit as st
import google.generativeai as genai
import os

def configurar_neurona():
    """Configura la conexión con la máxima seguridad."""
    # Prioridad 1: Secrets de Streamlit (Nube) | Prioridad 2: Archivo local (PC)
    api_key = st.secrets.get("API_KEY_QUEVEDO")
    if not api_key:
        try:
            import config
            api_key = config.API_KEY_QUEVEDO
        except ImportError:
            api_key = None
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

def consultar_especialista(pregunta_paciente, contexto_previo=""):
    """
    Activa al especialista médico de alto nivel.
    Inyectamos un 'System Prompt' que define su personalidad y conocimientos.
    """
    if not configurar_neurona():
        return "⚠️ Error de conexión: La neurona no tiene acceso a la API Key."

    # --- EL CEREBRO DEL ESPECIALISTA (SYSTEM INSTRUCTION) ---
    instrucciones_maestras = (
        "Actúa como el Director Médico del Consultorio Quevedo, un especialista de élite "
        "con conocimientos avanzados en medicina interna, cardiología y gestión de salud. "
        "Tu objetivo es analizar datos de pacientes, interpretar tendencias de presión y glucosa, "
        "y ofrecer orientación clínica basada en evidencia. "
        "Sé profesional, preciso, humano pero analítico. "
        "Si el usuario te da datos del 'Archivador' o de 'Salud', relaciónalos para dar un diagnóstico preventivo."
    )

    try:
        # Usamos el modelo más potente disponible
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash', # O 'gemini-1.5-pro' para máxima escala
            system_instruction=instrucciones_maestras
        )
        
        # Iniciamos un chat para que tenga memoria de la conversación
        chat = model.start_chat(history=[])
        
        prompt_final = f"Contexto del paciente: {contexto_previo}\n\nPregunta/Caso: {pregunta_paciente}"
        
        respuesta = chat.send_message(prompt_final)
        return respuesta.text

    except Exception as e:
        return f"❌ La neurona encontró un obstáculo: {str(e)}"
