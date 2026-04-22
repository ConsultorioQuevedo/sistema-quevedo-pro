import sqlite3
import os

def inicializar_todo():
    """
    Crea la conexión y las tablas necesarias.
    Funciona tanto en C:/ como en la nube de Streamlit.
    """
    # Intentamos usar la ruta de tu PC, si falla (porque estamos en la nube), usamos la ruta local
    try:
        if not os.path.exists("C:/sistema_quevedo"):
            db_path = "sistema_quevedo.db"
        else:
            db_path = "C:/sistema_quevedo/sistema_quevedo.db"
    except:
        db_path = "sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # --- CREACIÓN DE TABLAS (Para que nada falle al cargar módulos) ---
    c.execute('''CREATE TABLE IF NOT EXISTS glucosa 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, valor REAL, unidad TEXT, estado TEXT, fecha TEXT, hora TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, categoria TEXT, monto REAL, fecha TEXT)''')
    
    conn.commit()
    return conn, c
