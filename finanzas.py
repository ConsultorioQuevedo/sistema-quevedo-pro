import streamlit as st
import pandas as pd
from datetime import datetime
import base_datos as db
import logger_quevedo as log  # <--- Añadido: Registro de eventos
import seguridad_quevedo as seg # <--- Añadido: Escudo de seguridad

def mostrar_finanzas(conn, c):
    # Verificación de seguridad silenciosa
    seg.EscudoSeguridad.asegurar_carpetas()

    st.header("💰 FINANZA DE LUIS R QUEVEDO")
    st.divider()
    
    # 1. ENTRADA DE DATOS
    tipo = st.radio("Tipo de Movimiento", ["Ingreso", "Gasto"], horizontal=True)
    monto_input = st.text_input("Monto (RD$)")
    
    # Categoría se une a la descripción para no romper la base de datos
    categoria = st.selectbox("Categoría", ["Salud", "Alimentos", "Servicios", "Otros"])
    desc_base = st.text_input("Descripción")
    descripcion_total = f"[{categoria}] {desc_base}"

    if st.button("Registrar Transacción"):
        es_valido, resultado = db.validar_monto(monto_input)
        
        if es_valido:
            monto_final = resultado if tipo == "Ingreso" else -resultado
            try:
                # INSERT exacto en C:/
                c.execute("INSERT INTO finanzas (fecha, descripcion, monto, tipo) VALUES (?, ?, ?, ?)", 
                          (datetime.now().strftime("%Y-%m-%d"), descripcion_total, monto_final, tipo))
                conn.commit()
                
                # --- FUNCIÓN AÑADIDA: REGISTRO EN EL LOG ---
                log.registrar(f"TRANSACCIÓN: {tipo} de RD${resultado} - {categoria}")
                
                st.success(f"✅ {tipo} registrado por RD${resultado}")
                st.rerun() 
            except Exception as e:
                log.registrar(f"ERROR FINANZAS: {e}")
                st.error(f"Error al guardar en base de datos: {e}")
        else:
            st.error(resultado)

    st.divider()

    # 2. VISUALIZACIÓN E INTELIGENCIA DE BORRADO
    try:
        # Traemos el ID para poder borrar
        df = pd.read_sql_query("SELECT id, fecha, descripcion, monto, tipo FROM finanzas ORDER BY id DESC", conn)
        
        if not df.empty:
            st.subheader("📊 Historial de Movimientos")
            
            # Encabezados de la tabla dinámica
            head_col1, head_col2, head_col3, head_col4 = st.columns([1, 3, 1, 1])
            head_col1.write("**Fecha**")
            head_col2.write("**Descripción**")
            head_col3.write("**Monto**")
            head_col4.write("**Acción**")
            st.markdown("---")

            # Generamos una fila con botón de borrado por cada registro
            for index, row in df.iterrows():
                col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
                
                col1.write(row['fecha'])
                col2.write(row['descripcion'])
                
                # Color según sea ingreso o gasto
                color = "green" if row['monto'] > 0 else "red"
                col3.markdown(f"<span style='color:{color}'>RD$ {row['monto']:,.2f}</span>", unsafe_allow_html=True)
                
                # BOTÓN DE BORRADO
                if col4.button("🗑️", key=f"del_{row['id']}"):
                    if db.eliminar_registro("finanzas", row['id']):
                        # --- FUNCIÓN AÑADIDA: LOG DE BORRADO ---
                        log.registrar(f"ELIMINADO: Transacción ID {row['id']} de RD$ {row['monto']}")
                        st.warning(f"Registro {row['id']} eliminado")
                        st.rerun()

            st.divider()
            # Balance rápido
            balance = df['monto'].sum()
            st.metric("Balance Neto Actual", f"RD$ {balance:,.2f}")
        else:
            st.info("Aún no hay movimientos registrados.")
            
    except Exception as e:
        log.registrar(f"ERROR LECTURA FINANZAS: {e}")
        st.error(f"Error al leer el historial: {e}")
