import streamlit as st
import pandas as pd
from datetime import datetime

def mostrar_archivador(conn, c):
    st.header("📂 ARCHIVADOR INTELIGENTE IA")
    
    # 1. ESCÁNER Y CARGA
    with st.expander("📷 SUBIR DOCUMENTO O ANÁLISIS", expanded=True):
        archivo = st.file_uploader("Seleccione archivo (JPG, PNG, PDF)", type=['png', 'jpg', 'jpeg', 'pdf'])
        
        col1, col2 = st.columns(2)
        tipo_doc = col1.selectbox("Tipo", ["Receta", "Factura", "Laboratorio", "Personal"])
        etiquetas = col2.text_input("Etiquetas (ej: Glucosa, Dr. Perez)")
        
        if st.button("🚀 GUARDAR EN NUBE LOCAL"):
            if archivo is not None:
                try:
                    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                    # INSERT corregido
                    c.execute("""
                        INSERT INTO archivador (fecha, nombre_archivo, tipo, etiquetas) 
                        VALUES (?, ?, ?, ?)
                    """, (fecha_hoy, archivo.name, tipo_doc, etiquetas))
                    conn.commit()
                    st.success(f"✅ Documento '{archivo.name}' archivado.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("⚠️ Por favor, suba un archivo primero.")

    st.divider()

    # 2. BUSCADOR INTELIGENTE
    st.subheader("🔍 BUSCADOR DE ARCHIVOS")
    busqueda = st.text_input("Filtrar por nombre o etiqueta...")

    try:
        # Leemos la tabla
        df = pd.read_sql_query("SELECT * FROM archivador ORDER BY fecha DESC", conn)
        
        if not df.empty:
            if busqueda:
                # Filtro de búsqueda
                df = df[df['nombre_archivo'].str.contains(busqueda, case=False) | 
                        df['etiquetas'].str.contains(busqueda, case=False)]
            
            st.dataframe(df, use_container_width=True)
            
            # 3. BOTÓN DE LIMPIEZA
            if st.button("🧹 VACIAR ARCHIVADOR"):
                c.execute("DELETE FROM archivador")
                conn.commit()
                st.warning("Archivador vaciado.")
                st.rerun()
        else:
            st.info("El archivador está vacío. Sube tu primer documento arriba.")
    except Exception as e:
        st.error("⚠️ La tabla 'archivador' no existe. Debes crearla en base_datos.py")
