import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import base_datos as db

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.set_text_color(0, 34, 68) 
        self.cell(0, 10, 'SISTEMA QUEVEDO - REPORTE DE SALUD', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def generar_reporte_pdf(df):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 10)
    
    # Ajustamos las columnas a lo que realmente tienes en la base de datos
    columnas = ['Fecha', 'Glucosa', 'Presion', 'Notas']
    anchos = [40, 30, 40, 80]
    
    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 10, col, 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 9)
    for index, row in df.iterrows():
        # Notas: Manejo de texto seguro para latin-1
        notas_raw = str(row['notas']) if row['notas'] else "Sin notas"
        notas_seguro = notas_raw.encode('latin-1', 'replace').decode('latin-1')

        pdf.cell(anchos[0], 8, str(row['fecha']), 1)
        pdf.cell(anchos[1], 8, str(row['glucosa']), 1, 0, 'C')
        pdf.cell(anchos[2], 8, str(row['presion']), 1, 0, 'C')
        pdf.cell(anchos[3], 8, notas_seguro, 1)
        pdf.ln()

    return pdf.output(dest='S').encode('latin-1', 'replace')

def mostrar_pdf(conn):
    st.header("📄 Generador de Reportes Profesionales")
    st.info("Exporta tu historial de salud de forma segura.")

    try:
        # CORRECCIÓN DE LA CONSULTA: Quitamos 'hora' y 'estado' que no existen
        query = "SELECT fecha, glucosa, presion, notas FROM salud ORDER BY fecha DESC"
        df = pd.read_sql_query(query, conn)

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            if st.button("🚀 Crear Reporte PDF"):
                pdf_bytes = generar_reporte_pdf(df)
                st.download_button(
                    label="⬇️ Descargar Reporte",
                    data=pdf_bytes,
                    file_name=f"Reporte_Quevedo_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("No hay datos para reportar.")
    except Exception as e:
        st.error(f"Error en el módulo de PDF: {e}")
