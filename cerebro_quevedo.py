import google.generativeai as genai
import pandas as pd
import sqlite3

# --- LA NUEVA LLAVE MAESTRA ---
API_KEY = "AIzaSyB9tbJzUuo6TjgaWbu70ph93c_HUtfUW7o"

def conectar_neurona():
    try:
        genai.configure(api_key=API_KEY)
        
        # Intentamos los 3 nombres posibles para evitar el error 404
        for nombre_modelo in ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(nombre_modelo)
                # Prueba rápida de vida
                model.generate_content("test") 
                print(f"✅ Neurona activada con: {nombre_modelo}")
                return model
            except:
                continue
        return None
    except Exception as e:
        print(f"Error de configuración: {e}")
        return None

# Inicializamos el modelo
model = conectar_neurona()

def obtener_analisis_ia(conn):
    try:
        df_finanzas = pd.read_sql_query("SELECT * FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        resumen = df_finanzas.to_dict('records') if not df_finanzas.empty else "Sin datos"
        
        if model:
            response = model.generate_content(f"Soy Luis Quevedo. Analiza mis finanzas: {resumen}")
            return response.text
        return "La neurona sigue en modo espera."
    except Exception as e:
        return f"Glitch: {e}"

def procesar_consulta_asistente(consulta, conn):
    # Si el modelo no cargó al inicio, reintentamos
    global model
    if not model: model = conectar_neurona()
    
    try:
        if model:
            response = model.generate_content(f"Luis pregunta: {consulta}")
            return response.text
        return "No hay conexión con la neurona. Revisa tu internet o la API Key."
    except Exception as e:
        return f"Error en chat: {e}"
