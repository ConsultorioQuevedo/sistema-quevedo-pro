import streamlit as st
import cerebro_quevedo as cq
import os

def mostrar_inicio(conn):
    # --- 1. LÓGICA DEL LOG EN EL MENÚ LATERAL (Corregido para acentos) ---
    st.sidebar.title("🛠️ PANEL DE CONTROL")
    
    if st.sidebar.button("📋 Ver Log del Sistema"):
        st.sidebar.divider()
        st.sidebar.subheader("Registro de Eventos (Caja Negra)")
        
        # Ruta al archivo de log en tu Disco C
        log_path = "C:/sistema_quevedo/sistema_quevedo.log"
        
        if os.path.exists(log_path):
            try:
                # CAMBIO CLAVE: Usamos latin-1 para evitar errores con acentos
                with open(log_path, "r", encoding="latin-1") as f:
                    lineas = f.readlines()
                    # Mostramos las últimas 20 líneas para ver lo más reciente
                    texto_log = "".join(lineas[-20:])
                    st.sidebar.text_area("Historial reciente", value=texto_log, height=350)
            except Exception as e:
                st.sidebar.error(f"Error al leer log: {e}")
        else:
            st.sidebar.warning("El archivo de registro aún no se ha creado.")
            
    if st.sidebar.button("🧹 Limpiar Pantalla"):
        st.rerun()

    # --- 2. ESTILOS CSS PROFESIONALES (Estructura original intacta) ---
    st.markdown("""
        <style>
        .main-header {
            background-color: white;
            border: 2px solid #1e56a0;
            border-radius: 20px;
            padding: 20px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
        }
        .neurona-header {
            background: linear-gradient(135deg, #6a1b9a 0%, #4a148c 100%);
            color: white;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 20px;
            text-align: center;
            border-left: 8px solid #ea80fc;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
        .card {
            border-radius: 15px;
            padding: 20px;
            height: 180px;
            text-align: center;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
        }
        .card-title { font-weight: bold; font-size: 14px; margin-bottom: 10px; text-transform: uppercase; }
        .card-value { font-size: 24px; font-weight: bold; margin-bottom: 5px; }
        .card-footer { font-size: 11px; opacity: 0.9; margin-top: 10px; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 5px; }
        </style>
    """, unsafe_allow_html=True)

    # --- 3. ACTIVACIÓN DEL CEREBRO ---
    try:
        diagnostico, balance, consejo_ia = cq.obtener_datos_maestros(conn)
    except:
        # Fallback por si hay problemas con la IA
        diagnostico = "Pendiente"
        balance = 0.0
        consejo_ia = "Iniciando neuronas de Gemini... Listo para analizar, Luis."

    # --- 4. CONTENEDOR PRINCIPAL ---
    st.markdown(f"""
        <div class="main-header">
            <h1 style="color: #1e56a0; font-size: 30px; margin: 0;">Sistema Quevedo Pro</h1>
            <p style="color: #555; margin: 5px 0; font-weight: bold;">Desarrollado por Luis Rafael Quevedo</p>
            <p style="color: #888; font-style: italic; font-size: 14px; margin-top: 10px;">
                "Dedicado con todo mi amor a Eligia Morlas de Quevedo"
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. BLOQUE DE LA NEURONA (Gemini) ---
    st.markdown(f"""
        <div class="neurona-header">
            <div style="font-size: 12px; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 5px;">🧠 Neurona de Gemini Activa</div>
            <div style="font-size: 16px; font-style: italic;">"{consejo_ia}"</div>
        </div>
    """, unsafe_allow_html=True)

    # --- 6. FILA DE TARJETAS (3 Columnas) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="card" style="background-color: #28a745;">
                <div class="card-title">🩺 BIOMONITOR</div>
                <div class="card-value">{diagnostico}</div>
                <div class="card-footer">Estado de Salud en Tiempo Real</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="card" style="background-color: #007bff;">
                <div class="card-title">💰 BALANCE TOTAL</div>
                <div class="card-value">RD$ {balance:,.2f}</div>
                <div class="card-footer">Datos Sincronizados con Disco C</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="card" style="background-color: #f0ad4e;">
                <div class="card-title">🤖 ASISTENTE IA</div>
                <div class="card-value">Activo</div>
                <div class="card-footer">Cerebro_Quevedo v3.0 Nivel Dios</div>
            </div>
        """, unsafe_allow_html=True)

    # Pie de página
    st.markdown("<br><p style='text-align: center; color: #666; font-size: 14px;'>📍 Conectado a C:/sistema_quevedo | Luis Rafael Quevedo</p>", unsafe_allow_html=True)
