import sqlite3
import os

def inicializar_todo():
    # Ruta universal (PC y Nube)
    db_dir = "C:/sistema_quevedo"
    if not os.path.exists(db_dir):
        db_path = "sistema_quevedo.db"
    else:
        db_path = f"{db_dir}/sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # 1. Tabla SALUD
    c.execute('''CREATE TABLE IF NOT EXISTS salud 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, presion TEXT, glucosa REAL, notas TEXT)''')
    
    # 2. Tabla FINANZAS (Con la columna 'descripcion' que pedía el error)
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha TEXT, descripcion TEXT, monto REAL, tipo TEXT)''')
    
    # 3. Tabla ARCHIVADOR (Creada desde cero)
    c.execute('''CREATE TABLE IF NOT EXISTS archivador 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre_archivo TEXT, tipo TEXT, ruta TEXT, fecha TEXT)''')
    
    conn.commit()
    return conn, c

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
