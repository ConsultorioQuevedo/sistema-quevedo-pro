import google.generativeai as genai
import pandas as pd
import sqlite3
import os

# --- CONFIGURACIÓN DE LA NEURONA ---
API_KEY = "AIzaSyCBx-fT3KdAQnruDuaryU0sqli3PHqxEmU"

try:
    genai.configure(api_key=API_KEY)
    # Cambiamos a 'gemini-1.5-flash-latest' para solucionar el Error 404
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    model = None
    print(f"Error configurando la neurona: {e}")

def obtener_analisis_ia(conn):
    """
    Lee los datos reales de Luis y genera un diagnóstico inteligente.
    """
    try:
        # 1. Extraer datos para que la IA sepa de qué habla
        df_salud = pd.read_sql_query("SELECT glucosa, presion FROM salud ORDER BY id DESC LIMIT 1", conn)
        df_finanzas = pd.read_sql_query("SELECT monto, descripcion, tipo FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        
        # 2. Resumen para el Prompt
        datos_salud = df_salud.to_dict('records') if not df_salud.empty else "Sin registros recientes"
        datos_finanzas = df_finanzas.to_dict('records') if not df_finanzas.empty else "Sin movimientos"
        
        # 3. El Prompt Maestro
        prompt = f"""
        Eres la 'Neurona Principal' del Sistema Quevedo Pro. 
        Tu usuario es Luis Rafael Quevedo, un experto en tecnología y bases de datos.
        
        Analiza estos datos actuales:
        - Salud: {datos_salud}
        - Finanzas: {datos_finanzas}
        
        Da un consejo breve, técnico y motivador. Si ves que hay ingresos (como los RD$257), 
        felicítalo por mantener el flujo de caja. No uses introducciones largas.
        """
        
        if model:
            # Usamos la configuración de generación estándar para evitar errores de versión
            response = model.generate_content(prompt)
            return response.text
        else:
            return "La neurona está en modo espera. Verifica la conexión a internet."

    except Exception as e:
        # Si falla el modelo Flash, intentamos con el Pro como respaldo
        return f"La neurona tiene un pequeño glitch: {str(e)}"

def procesar_consulta_asistente(consulta, conn):
    """
    Para el chat interactivo del módulo Asistente.
    """
    try:
        if model:
            # Iniciamos el chat con el modelo actualizado
            chat = model.start_chat(history=[])
            response = chat.send_message(f"Luis pregunta: {consulta}. Responde como el Sistema Quevedo.")
            return response.text
        return "IA no disponible por configuración de modelo."
    except Exception as e:
        # Este mensaje te dirá exactamente si el problema persiste
        return f"Error en chat: {e}"
