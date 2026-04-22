import google.generativeai as genai
import pandas as pd

# --- CONFIGURACIÓN CON TU LLAVE CONFIRMADA ---
API_KEY = "AIzaSyB9tbJzUuo6TjgaWbu70ph93c_HUtfUW7o"

def conectar_neurona():
    try:
        genai.configure(api_key=API_KEY)
        # Usamos uno de los modelos que tu terminal confirmó que tienes (2.0 Flash)
        # El nombre debe ser exacto como salió en tu lista
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        print(f"Error al conectar: {e}")
        return None

# Inicializamos la neurona
model = conectar_neurona()

def obtener_analisis_ia(conn):
    try:
        df_f = pd.read_sql_query("SELECT monto, descripcion FROM finanzas ORDER BY id DESC LIMIT 5", conn)
        datos = df_f.to_dict('records') if not df_f.empty else "Sin movimientos"
        
        if model:
            # Agregamos una instrucción clara para que la IA sepa quién eres
            prompt = f"Luis Quevedo, experto en tecnología. Analiza mis finanzas: {datos}. Dame un consejo motivador corto."
            response = model.generate_content(prompt)
            return response.text
        return "La neurona está esperando órdenes."
    except Exception as e:
        return f"Error en análisis: {str(e)}"

def procesar_consulta_asistente(consulta, conn):
    global model
    if not model: model = conectar_neurona()
    
    try:
        if model:
            # Respuesta directa para el asistente
            response = model.generate_content(f"Usuario Luis Quevedo pregunta: {consulta}")
            return response.text
        return "No se pudo establecer conexión con Gemini 2.0."
    except Exception as e:
        return f"Error en el chat: {str(e)}"
