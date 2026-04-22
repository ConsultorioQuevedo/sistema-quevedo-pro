import google.generativeai as genai
import pandas as pd
import os

# --- CONFIGURACIÓN DE LA NEURONA ---
API_KEY = "AIzaSyCBx-fT3KdAQnruDuaryU0sqli3PHqxEmU"

def configurar_modelo():
    try:
        genai.configure(api_key=API_KEY)
        # 1. Buscamos qué modelos tienes permitidos usar
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if modelos_disponibles:
            # Seleccionamos el primero que aparezca (usualmente gemini-pro o flash)
            nombre_modelo = modelos_disponibles[0]
            print(f"✅ Neurona conectada usando: {nombre_modelo}")
            return genai.GenerativeModel(nombre_modelo)
        return None
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None

# Activamos el modelo al iniciar
model = configurar_modelo()

def obtener_analisis_ia(conn):
    try:
        df_salud = pd.read_sql_query("SELECT glucosa, presion FROM salud ORDER BY id DESC LIMIT 1", conn)
        df_finanzas = pd.read_sql_query("SELECT monto, descripcion, tipo FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        
        prompt = f"Luis Quevedo. Salud: {df_salud.to_dict()}. Finanzas: {df_finanzas.to_dict()}. Consejo técnico breve."
        
        if model:
            response = model.generate_content(prompt)
            return response.text
        return "La neurona sigue apagada. Revisa tu conexión."
    except Exception as e:
        return f"Error en análisis: {str(e)}"

def procesar_consulta_asistente(consulta, conn):
    global model
    if not model: # Reintento de conexión
        model = configurar_modelo()
        
    try:
        if model:
            response = model.generate_content(f"Usuario: Luis Quevedo. Pregunta: {consulta}")
            return response.text
        return "No se encontró ningún modelo compatible en tu cuenta de Google."
    except Exception as e:
        return f"Error crítico: {e}"
