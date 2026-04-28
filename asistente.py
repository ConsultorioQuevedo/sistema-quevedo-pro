import streamlit as st
import cerebro_quevedo as cerebro

def mostrar_asistente(conn, c):
    st.title("🧠 Neurona Interactiva - Sistema Quevedo")
    st.write("Consulta lo que necesites sobre tus finanzas, salud o tecnología.")

    # 1. Inicializar la memoria del chat para que no se "muera" al refrescar
    if "historial_chat" not in st.session_state:
        st.session_state.historial_chat = []

    # 2. Área de chat
    with st.container():
        for mensaje in st.session_state.historial_chat:
            with st.chat_message(mensaje["role"]):
                st.markdown(mensaje["content"])

    # 3. Entrada de texto (El botón de envío ya no estará muerto)
    if prompt := st.chat_input("¿En qué puedo ayudarte, Luis?"):
        # Mostrar mensaje del usuario
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.historial_chat.append({"role": "user", "content": prompt})

        # Llamar a la neurona (cerebro_quevedo.py)
        with st.chat_message("assistant"):
            with st.spinner("La neurona está procesando..."):
                respuesta = cerebro.procesar_consulta_asistente(prompt, conn)
                st.markdown(respuesta)
        
        st.session_state.historial_chat.append({"role": "assistant", "content": respuesta})

    # 4. Botones de acción rápida (Ya no serán estáticos)
    st.sidebar.subheader("Acciones Rápidas")
    if st.sidebar.button("📊 Analizar mis Gastos"):
        consulta = "Haz un resumen de mis últimos gastos de finanzas y dime si voy bien."
        # Forzamos la ejecución
        respuesta = cerebro.procesar_consulta_asistente(consulta, conn)
        st.info(respuesta)

    if st.sidebar.button("🏥 Estado de Salud"):
        consulta = "Analiza mis últimos datos de salud y dame un consejo."
        respuesta = cerebro.procesar_consulta_asistente(consulta, conn)
        st.success(respuesta)
