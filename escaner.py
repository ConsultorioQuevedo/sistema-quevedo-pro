import streamlit as st
import pytesseract
from PIL import Image
import io
from datetime import datetime

def mostrar_escaner(conn, c, ZONA_HORARIA):
    st.header("📸 Escáner de Documentos IA")
    st.write("Digitaliza facturas, recetas o documentos importantes.")

    # --- CAPTURA DE IMAGEN ---
    opcion = st.radio("Fuente de imagen:", ["Cámara en vivo", "Subir archivo"], horizontal=True)
    
    img_file = None
    if opcion == "Cámara en vivo":
        img_file = st.camera_input("Enfoque el documento")
    else:
        img_file = st.file_uploader("Seleccione imagen", type=['jpg', 'png', 'jpeg'])

    if img_file:
        img = Image.open(img_file)
        st.image(img, caption="Imagen capturada", width=300)
        
        if st.button("🔍 PROCESAR Y EXTRAER TEXTO", use_container_width=True):
            with st.spinner("Analizando documento..."):
                try:
                    # Ejecutar OCR
                    texto_extraido = pytesseract.image_to_string(img, lang='spa')
                    
                    if texto_extraido.strip():
                        st.subheader("📝 Texto Detectado:")
                        st.text_area("Resultado:", texto_extraido, height=200)
                        
                        # --- GUARDAR EN BÚNKER ---
                        nombre_doc = f"SCAN_{datetime.now(ZONA_HORARIA).strftime('%Y%m%d_%H%M%S')}"
                        fecha_hoy = datetime.now(ZONA_HORARIA).strftime('%Y-%m-%d')
                        
                        c.execute("INSERT INTO archivos (nombre, tipo, fecha, texto_ocr) VALUES (?, ?, ?, ?)",
                                  (nombre_doc, "SCAN", fecha_hoy, texto_extraido))
                        conn.commit()
                        
                        st.success(f"✅ Guardado en el Archivador como: {nombre_doc}")
                    else:
                        st.warning("No se pudo extraer texto legible. Intente con más luz.")
                except Exception as e:
                    st.error(f"Error técnico en el motor OCR: {e}")
                    st.info("Nota: Asegúrese de tener Tesseract instalado en su sistema.")

    st.divider()
    st.caption("Tecnología de Reconocimiento Óptico de Caracteres (OCR) integrada.")
