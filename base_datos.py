import sqlite3
import os

def inicializar_todo():
    # 1. Definición de rutas (Mantiene tu lógica de Disco C)
    db_dir = "C:/sistema_quevedo"
    if not os.path.exists(db_dir):
        db_path = "sistema_quevedo.db"
    else:
        db_path = f"{db_dir}/sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # 2. Creación de tablas (Estructura completa y sincronizada)
    
    # Tabla SALUD
    c.execute('''CREATE TABLE IF NOT EXISTS salud 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  fecha TEXT, 
                  presion TEXT, 
                  glucosa REAL, 
                  notas TEXT)''')
    
    # Tabla FINANZAS (Incluye 'descripcion' para evitar el error de los logs)
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  fecha TEXT, 
                  descripcion TEXT, 
                  monto REAL, 
                  tipo TEXT)''')
    
    # Tabla ARCHIVADOR
    c.execute('''CREATE TABLE IF NOT EXISTS archivador 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  nombre_archivo TEXT, 
                  tipo TEXT, 
                  ruta TEXT, 
                  fecha TEXT)''')
    
    conn.commit()
    return conn, c

# --- FUNCIÓN INSERTADA (La que faltaba y causaba el AttributeError) ---
def validar_monto(monto):
    """
    Verifica que el monto ingresado sea un número válido y mayor a cero.
    Retorna (True, monto) si es correcto, (False, mensaje) si hay error.
    """
    try:
        valor = float(monto)
        if valor <= 0:
            return False, "El monto debe ser mayor a cero."
        return True, valor
    except (ValueError, TypeError):
        return False, "Por favor, ingrese un número válido."

def eliminar_registro(tabla, id_reg):
    try:
        # Busca la base de datos en la ruta que corresponda
        db_path = "C:/sistema_quevedo/sistema_quevedo.db" if os.path.exists("C:/sistema_quevedo") else "sistema_quevedo.db"
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_reg,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False
