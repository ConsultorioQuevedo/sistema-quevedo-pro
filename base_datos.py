import sqlite3
import streamlit as st
import os

# Definimos la ruta absoluta para evitar que el asistente se pierda
DB_PATH = r'C:\sistema_quevedo\sistema_quevedo.db'

def conectar():
    """Conexión robusta con manejo de errores de ruta."""
    try:
        # Aseguramos que la carpeta existe
        if not os.path.exists(r'C:\sistema_quevedo'):
            os.makedirs(r'C:\sistema_quevedo')
        return sqlite3.connect(DB_PATH, check_same_thread=False)
    except sqlite3.Error as e:
        st.error(f"Error crítico de conexión: {e}")
        return None

def inicializar_todo():
    """Sincroniza la estructura de 5 columnas sin tocar tus datos."""
    conn = conectar()
    if conn:
        c = conn.cursor()
        # Tabla Salud: ID, FECHA, PRESION, GLUCOSA, NOTAS
        c.execute('''CREATE TABLE IF NOT EXISTS salud (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     fecha TEXT, 
                     presion TEXT, 
                     glucosa INTEGER, 
                     notas TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS finanzas (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     fecha TEXT, descripcion TEXT, monto REAL, tipo TEXT)''')
        
        conn.commit()
        return conn, c
    return None, None

def validar_monto(monto_texto):
    """Valida que el monto sea un número válido para Finanzas."""
    try:
        monto_limpio = monto_texto.replace(',', '.').strip()
        valor_final = float(monto_limpio)
        if valor_final < 0:
            return False, "El monto no puede ser negativo."
        return True, valor_final
    except ValueError:
        return False, "Por favor, introduce un número válido (ej: 1200.50)."

# --- FUNCIÓN NUEVA: EL MOTOR DE BORRADO ---
def eliminar_registro(tabla, registro_id):
    """
    Esta función permite que cualquier módulo borre un dato.
    Uso: db.eliminar_registro('salud', 5)
    """
    try:
        conn = conectar()
        c = conn.cursor()
        # Usamos f-string para la tabla pero parámetros seguros para el ID
        c.execute(f"DELETE FROM {tabla} WHERE id = ?", (registro_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error al intentar borrar en {tabla}: {e}")
        return False
