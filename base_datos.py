import sqlite3
import os

def inicializar_todo():
    try:
        if not os.path.exists("C:/sistema_quevedo"):
            db_path = "sistema_quevedo.db"
        else:
            db_path = "C:/sistema_quevedo/sistema_quevedo.db"
    except:
        db_path = "sistema_quevedo.db"

    conn = sqlite3.connect(db_path, check_same_thread=False)
    c = conn.cursor()

    # TABLA SALUD (Ajustada a lo que pide tu Biomonitor)
    c.execute('''CREATE TABLE IF NOT EXISTS salud 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  fecha TEXT, 
                  presion TEXT, 
                  glucosa REAL, 
                  notas TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS finanzas 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, categoria TEXT, monto REAL, fecha TEXT)''')
    
    conn.commit()
    return conn, c

def eliminar_registro(tabla, id_registro):
    try:
        # Esta es la pieza que faltaba para que el botón de borrar funcione
        conn, c = inicializar_todo()
        c.execute(f"DELETE FROM {tabla} WHERE id = ?", (id_registro,))
        conn.commit()
        conn.close()
        return True
    except:
        return False
