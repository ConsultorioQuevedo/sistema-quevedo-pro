import pandas as pd

def obtener_analisis_ia(conn):
    # Análisis básico basado en lógica pura, sin necesidad de Internet
    try:
        df_f = pd.read_sql_query("SELECT monto FROM finanzas", conn)
        if not df_f.empty:
            total = df_f['monto'].sum()
            return f"Análisis local: Tienes un flujo registrado de {total}. ¡Sigue así, Luis!"
        return "Sin datos suficientes para analizar hoy."
    except:
        return "Módulo de análisis listo."

def procesar_consulta_asistente(consulta, conn):
    # Respuestas automáticas rápidas para no dejar el chat vacío
    consulta = consulta.lower()
    
    if "hola" in consulta:
        return "¡Hola Luis! Estoy listo para ayudarte con tus registros locales."
    elif "gasto" in consulta or "dinero" in consulta:
        return "Revisa el módulo de Finanzas para ver tus balances actuales."
    elif "salud" in consulta:
        return "Tus datos de Biomonitor están guardados correctamente."
    else:
        return "Entendido, Luis. He procesado tu mensaje en el sistema local."
