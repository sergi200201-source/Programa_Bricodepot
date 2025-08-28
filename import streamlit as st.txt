import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os

ARCHIVO = "datos.xlsx"
COLUMNAS = ["Nombre Cliente", "Número SAP", "Estado Pedido", "DNI", "Teléfono"]

# Autenticación simple
def autenticar():
    with st.form("login"):
        usuario = st.text_input("Introduce tu nombre de usuario:")
        enviar = st.form_submit_button("Entrar")
        if enviar:
            if usuario.strip().lower() == "sergi":
                st.session_state["autenticado"] = True
                st.success(f"¡Bienvenido al PROGRAMA DE BRICO DEPÔT, {usuario}!")
            else:
                st.error("No estás autorizado para acceder a este programa.")

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    autenticar()
    st.stop()

st.title("PROGRAMA DE BRICO DEPÔT")

# Selección de modo
modo = st.radio("Selecciona una opción:", ["Editar pedidos", "Consultar pedidos"])

# Cargar datos de Excel o crear archivo si no existe
if os.path.exists(ARCHIVO):
    df = pd.read_excel(ARCHIVO)
else:
    df = pd.DataFrame(columns=COLUMNAS)
    df.to_excel(ARCHIVO, index=False)

if modo == "Editar pedidos":
    st.subheader("Tabla editable de pedidos")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=True)
    grid_options = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        editable=True,
        fit_columns_on_grid_load=True,
        height=350
    )

    # Botón para guardar cambios en Excel
    if st.button("Guardar cambios en Excel"):
        datos_editados = pd.DataFrame(grid_response["data"])
        datos_editados.to_excel(ARCHIVO, index=False)
        st.success("¡Datos guardados en Excel!")

    # Botón para añadir nueva fila vacía
    if st.button("Añadir nueva fila"):
        nueva_fila = pd.DataFrame([["", "", "", "", ""]], columns=COLUMNAS)
        df = pd.concat([pd.DataFrame(grid_response["data"]), nueva_fila], ignore_index=True)
        df.to_excel(ARCHIVO, index=False)
        st.experimental_rerun()

elif modo == "Consultar pedidos":
    st.subheader("Consulta de pedidos (solo lectura)")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(editable=False)
    grid_options = gb.build()

    AgGrid(
        df,
        gridOptions=grid_options,
        editable=False,
        fit_columns_on_grid_load=True,
        height=350
    )