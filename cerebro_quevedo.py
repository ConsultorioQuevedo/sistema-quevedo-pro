import google.generativeai as genai
import pandas as pd
import sqlite3
import os

# --- CONFIGURACIÓN DE LA NEURONA ---
API_KEY = "AIzaSyCBx-fT3KdAQnruDuaryU0sqli3PHqxEmU"

try:
    genai.configure(api_key=API_KEY)
    # Usamos 'gemini-pro' porque tu sistema está pidiendo estabilidad sobre novedad
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    model = None
    print(f"Error configurando la neurona: {e}")

def obtener_analisis_ia(conn):
    try:
        df_salud = pd.read_sql_query("SELECT glucosa, presion FROM salud ORDER BY id DESC LIMIT 1", conn)
        df_finanzas = pd.read_sql_query("SELECT monto, descripcion, tipo FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        
        datos_salud = df_salud.to_dict('records') if not df_salud.empty else "Sin registros"
        datos_finanzas = df_finanzas.to_dict('records') if not df_finanzas.empty else "Sin movimientos"
        
        prompt = f"Luis Quevedo (Desarrollador). Salud: {datos_salud}. Finanzas: {datos_finanzas}. Da un consejo breve y técnico."
        
        if model:
            response = model.generate_content(prompt)
            return response.text
        return "IA en espera."
    except Exception as e:
        return f"Glitch en neurona: {str(e)}"

def procesar_consulta_asistente(consulta, conn):
    try:
        if model:
            # En gemini-pro la estructura de chat es la más robusta
            chat = model.start_chat(history=[])
            response = chat.send_message(f"Luis pregunta: {consulta}")
            return response.text
        return "IA no disponible."
    except Exception as e:
        # Si el 404 persiste, este bloque atrapará el error y te dirá qué pasó
        return f"Error en chat: {e}"
