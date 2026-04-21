import logging
import os

# Definimos la ruta en tu Disco C
LOG_DIR = "C:/sistema_quevedo"
LOG_FILE = os.path.join(LOG_DIR, "sistema_quevedo.log")

# Creamos la carpeta si no existe
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuración del motor de registro
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def registrar(mensaje):
    """Escribe un evento en el log y en la consola."""
    logging.info(mensaje)
    print(f"🕵️ Sistema Quevedo Log: {mensaje}")
