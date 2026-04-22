import sqlite3
import os

def inicializar_todo():
    # 1. Rutas
    db_dir = "C:/sistema_quevedo"
    if not os.path.exists(db_dir):
        db_path = "sistema_quevedo.db"
    else:
        db_path = f"{db_dir}/sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # 2. CREACIÓN DE TABLAS (Estructura base)
    c.execute('''CREATE TABLE IF NOT EXISTS salud 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, presion TEXT, glucosa REAL, notas TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, monto REAL, tipo TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS archivador 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre_archivo TEXT, tipo TEXT, ruta TEXT, fecha TEXT)''')

    # --- 3. EL ARREGLO MAESTRO (Para que no falle el INSERT) ---
    # Intentamos agregar la columna 'descripcion' si no existe
    try:
        c.execute("ALTER TABLE finanzas ADD COLUMN descripcion TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        # Si ya existe, no hace nada y no da error
        pass

    conn.commit()
    return conn, c

def validar_monto(monto):
    try:
        valor = float(monto)
        if valor <= 0: return False, "El monto debe ser mayor a cero."
        return True, valor
    except:
        return False, "Por favor, ingrese un número válido."

def eliminar_registro(tabla, id_reg):
    try:
        db_path = "C:/sistema_quevedo/sistema_quevedo.db" if os.path.exists("C:/sistema_quevedo") else "sistema_quevedo.db"
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_reg,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
