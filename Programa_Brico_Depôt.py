import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import os

#Titulo del programa 
st.title("📦 Programa Bricodepot")
st.subheader("Gestión eficiente de productos y presupuestos")
#Sidebar 
st.sidebar.image("logo.png", width=150)
st.sidebar.header("Opciones")
#Style 
st.markdown("<style>...</style>", unsafe_allow_html=True)

ARCHIVO = "datos.xlsx"
COLUMNAS = ["Nombre Cliente", "Número SAP", "Estado Pedido", "DNI", "Teléfono"]

# --- Autenticación simple ---
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

# --- Cargar datos de Excel o crear archivo si no existe ---
if os.path.exists(ARCHIVO):
    df = pd.read_excel(ARCHIVO, dtype={"Teléfono": str})
else:
    df = pd.DataFrame(columns=COLUMNAS)
    df.to_excel(ARCHIVO, index=False)

# --- Inicializar variable de sesión para la vista ---
if "vista" not in st.session_state:
    st.session_state["vista"] = None

# --- Selección de modo con botones ---
col1, col2, col3 = st.columns(3)
with col1:
    if st.sidebar.button("Editar pedidos"):
        st.session_state["vista"] = "editar"
with col2:
    if st.sidebar.button("Consultar pedidos"):
        st.session_state["vista"] = "consultar"
with col3:
    if st.sidebar.button("Nueva entrada"):
        st.session_state["vista"] = "nueva"

# --- Barra de búsqueda ---
def filtrar_dataframe(df):
    st.markdown("### Buscar pedido")
    busqueda = st.text_input("Buscar por nombre, número SAP, teléfono o DNI:")
    if busqueda:
        busqueda = busqueda.lower()
        mask = (
            df["Nombre Cliente"].str.lower().str.contains(busqueda) |
            df["Número SAP"].astype(str).str.lower().str.contains(busqueda) |
            df["Teléfono"].astype(str).str.lower().str.contains(busqueda) |
            df["DNI"].str.lower().str.contains(busqueda)
        )
        return df[mask]
    return df

# --- Mostrar solo el contenido seleccionado ---
if st.session_state["vista"] == "editar":
    st.subheader("Tabla editable de pedidos")
    df_filtrado = filtrar_dataframe(df)
    gb = GridOptionsBuilder.from_dataframe(df_filtrado)
    gb.configure_default_column(editable=True)
    gb.configure_column(
        "Estado Pedido",
        editable=True,
        cellEditor='agSelectCellEditor',
        cellEditorParams={
            "values": ["pendiente", "pedido", "entregado", "incidencia", "solucionado"]
        }
    )
    grid_options = gb.build()

    grid_response = AgGrid(
        df_filtrado,
        gridOptions=grid_options,
        editable=True,
        fit_columns_on_grid_load=True,
        height=350
    )

    if st.button("Guardar cambios en Excel"):
        datos_editados = pd.DataFrame(grid_response["data"])
        datos_editados.to_excel(ARCHIVO, index=False)
        st.success("¡Datos guardados en Excel!")
        st.experimental_rerun()

    if st.button("Añadir nueva fila vacía"):
        nueva_fila = pd.DataFrame([["", "", "", "", ""]], columns=COLUMNAS)
        df = pd.concat([pd.DataFrame(grid_response["data"]), nueva_fila], ignore_index=True)
        df.to_excel(ARCHIVO, index=False)
        st.experimental_rerun()

elif st.session_state["vista"] == "consultar":
    st.subheader("Consulta de pedidos (solo lectura)")
    df_filtrado = filtrar_dataframe(df)
    gb = GridOptionsBuilder.from_dataframe(df_filtrado)
    gb.configure_default_column(editable=False)
    grid_options = gb.build()

    AgGrid(
        df_filtrado,
        gridOptions=grid_options,
        editable=False,
        fit_columns_on_grid_load=True,
        height=350
    )

elif st.session_state["vista"] == "nueva":
    st.subheader("Añadir nueva entrada")
    with st.form("nueva_entrada"):
        nombre_cliente = st.text_input("Nombre del cliente:")
        numero_sap = st.text_input("Número SAP:")
        estado_pedido = st.selectbox(
            "Estado del pedido:",
            ["pendiente", "pedido", "entregado", "incidencia", "solucionado"]
        )
        dni = st.text_input("DNI:")
        telefono = st.text_input("Teléfono:")
        enviar = st.form_submit_button("Guardar")
        if enviar:
            # Validación de campos
            if not all([nombre_cliente, numero_sap, estado_pedido, dni, telefono]):
                st.error("Por favor, completa todos los campos.")
            elif not (telefono.isdigit() and len(telefono) == 9):
                st.error("El teléfono debe contener exactamente 9 dígitos numéricos.")
            else:
                # Recarga el DataFrame desde el archivo antes de añadir la nueva fila
                if os.path.exists(ARCHIVO):
                    df = pd.read_excel(ARCHIVO)
                else:
                    df = pd.DataFrame(columns=COLUMNAS)
                nueva_fila = pd.DataFrame([[nombre_cliente, numero_sap, estado_pedido, dni, telefono]], columns=COLUMNAS)
                df = pd.concat([df, nueva_fila], ignore_index=True)
                df.to_excel(ARCHIVO, index=False)
                st.success("¡Datos guardados en Excel correctamente!")
                st.session_state["vista"] = "editar"
                st.experimental_rerun()

