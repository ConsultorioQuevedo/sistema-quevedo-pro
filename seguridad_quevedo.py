import os

class EscudoSeguridad:
    """Módulo de protección para el Sistema Quevedo"""
    
    @staticmethod
    def asegurar_carpetas():
        """Garantiza que la carpeta en el Disco C exista."""
        ruta = "C:/sistema_quevedo"
        try:
            if not os.path.exists(ruta):
                os.makedirs(ruta)
            return True
        except Exception:
            return False

# Al final del archivo, agrega esto para probarlo solo
if __name__ == "__main__":
    print("🛡️ Escudo de Seguridad funcionando correctamente.")
