import pandas as pd
import logger_quevedo as log
import google.generativeai as genai
import streamlit as st

def obtener_datos_maestros(conn):
    """
    Versión 'Cerebro Híbrido': Lee la base de datos y le pregunta a Gemini.
    """
    try:
        # 1. Obtener datos reales de la base de datos
        df_salud = pd.read_sql_query("SELECT presion, glucosa, fecha FROM salud ORDER BY id DESC LIMIT 1", conn)
        df_fin = pd.read_sql_query("SELECT SUM(monto) as total FROM finanzas", conn)
        
        hay_salud = not df_salud.empty
        balance_valor = df_fin['total'].iloc[0] if df_fin['total'].iloc[0] is not None else 0.0
        
        presion = df_salud['presion'].iloc[0] if hay_salud else "N/A"
        glucosa = df_salud['glucosa'].iloc[0] if hay_salud else "N/A"
        diagnostico = f"{presion} | {glucosa} mg" if hay_salud else "Esperando datos"

        # 2. INTENTO DE CONEXIÓN CON LA NEURONA (GEMINI)
        try:
            # Buscamos la clave en los Secrets de Streamlit o en config local
            if "API_KEY_QUEVEDO" in st.secrets:
                api_key = st.secrets["API_KEY_QUEVEDO"]
            else:
                import config
                api_key = config.API_KEY_QUEVEDO
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Le damos contexto a la IA para que te dé un consejo real
            prompt = f"""
            Actúa como el asistente del Sistema Quevedo Pro. 
            El usuario Luis tiene los siguientes datos:
            - Salud: Presión {presion}, Glucosa {glucosa}.
            - Finanzas: Balance RD$ {balance_valor:,.2f}.
            Dame un consejo motivador y breve (máximo 15 palabras).
            """
            response = model.generate_content(prompt)
            consejo_ia = response.text
            log.registrar("Neurona Gemini: Respuesta generada con éxito.")
            
        except Exception as e_ia:
            # Si falla la IA (por internet o falta de clave), usamos el mensaje de respaldo
            log.registrar(f"IA no disponible: {e_ia}")
            consejo_ia = "Sistema Quevedo Pro: El éxito es la suma de pequeños esfuerzos diarios. ¡Sigue adelante, Luis!"

    except Exception as e:
        log.registrar(f"Error general en el cerebro: {e}")
        diagnostico = "Listo"
        balance_valor = 0.0
        consejo_ia = "Bienvenido al Sistema Quevedo Pro, Luis."
        
    return diagnostico, balance_valor, consejo_ia
