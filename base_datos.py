import sqlite3
import os

def inicializar_todo():
    # Ruta universal (PC y Nube)
    if not os.path.exists("C:/sistema_quevedo"):
        db_path = "sistema_quevedo.db"
    else:
        db_path = "C:/sistema_quevedo/sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # Tabla SALUD (Para Biomonitor y PDF)
    c.execute('''CREATE TABLE IF NOT EXISTS salud 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  fecha TEXT, 
                  presion TEXT, 
                  glucosa REAL, 
                  notas TEXT)''')
    
    # Tabla FINANZAS (Para el módulo de Finanzas)
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  fecha TEXT, 
                  descripcion TEXT, 
                  monto REAL, 
                  tipo TEXT)''')
    
    conn.commit()
    return conn, c

def eliminar_registro(tabla, id_reg):
    try:
        if not os.path.exists("C:/sistema_quevedo"):
            db_path = "sistema_quevedo.db"
        else:
            db_path = "C:/sistema_quevedo/sistema_quevedo.db"
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_reg,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
