

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk


df = pd.read_excel("datos/dfDatosFinales3.xlsx")
st.header("ANÁLISIS DE MANGLARES EN LA ZONA SUR DE MÉXICO")
###################################################################
# Lista de estados posibles
estados_posibles = ['Yucatan', 'Campeche', 'Quintana Roo', 'Tamaulipas', 'Chiapas', 'Oaxaca']

# Especies específicas a incluir o excluir
especies_incluir = [
    "Avicennia germinans",
    "Laguncularia racemosa",
    "Rhizophora mangle",
    "Conocarpus erectus"
]

# Selectbox para elegir el estado
estado_seleccionado22 = st.selectbox("Selecciona un estado", estados_posibles, key="selectbox_estado22")

# Filtrar el DataFrame por el estado seleccionado
df_filtrado = df[df['ESTADO'] == estado_seleccionado22]

#
# Filtrar solo las especies seleccionadas
df_especies_incluir = df_filtrado[df_filtrado['ESPECIE'].isin(especies_incluir)]

# Agrupar por especie y contar las incidencias
df_especies_incluir = df_especies_incluir['ESPECIE'].value_counts().reset_index(name='CANTIDAD')
df_especies_incluir.columns = ['ESPECIE', 'CANTIDAD']

# Crear el gráfico de pastel para las especies específicas
fig1 = px.pie(
    df_especies_incluir,
    names='ESPECIE',
    values='CANTIDAD',
    title=f"Especies de manglar en {estado_seleccionado22}",
    labels={'CANTIDAD': 'Número de Ejemplares'}
)

# Mostrar el gráfico 1
st.plotly_chart(fig1, use_container_width=True, key="grafico_pastel_especiesManglar")
########################################
# Filtrar las especies que no están en la lista de especies_incluir
df_otras_especies = df_filtrado[~df_filtrado['ESPECIE'].isin(especies_incluir)]

# Verificar si el DataFrame no está vacío antes de crear el gráfico
if not df_otras_especies.empty:
    # Agrupar por especie y contar las incidencias
    df_otras_especies = df_otras_especies['ESPECIE'].value_counts().reset_index(name='CANTIDAD')
    df_otras_especies.columns = ['ESPECIE', 'CANTIDAD']

    # Crear el gráfico de pastel para las otras especies
    fig2 = px.pie(
        df_otras_especies,
        names='ESPECIE',
        values='CANTIDAD',
        title=f"Especies asociadas en {estado_seleccionado22}",
        labels={'CANTIDAD': 'Número de Ejemplares'}
    )

    # Mostrar el gráfico si hay datos
    st.plotly_chart(fig2, use_container_width=True, key="grafico_pastel_especiesAsociadas")
else:
    # Mostrar un mensaje de advertencia si no hay datos
    st.warning(f"No hay datos disponibles de especies asociadas en {estado_seleccionado22}.")
#############################################
estado_seleccionado = st.selectbox("Selecciona un estado", estados_posibles, key="selectbox_estado")

# Filtrar el DataFrame por el estado seleccionado
df_filtrado = df[df['ESTADO'] == estado_seleccionado]

# Agrupar por CARACTERÍSTICA y contar las incidencias
df_caracteristicas = df_filtrado['CARACTERÍSTICA'].value_counts().reset_index(name='CANTIDAD')
df_caracteristicas.columns = ['CARACTERÍSTICA', 'CANTIDAD']

# Crear la gráfica de pastel
fig = px.pie(
    df_caracteristicas,
    names='CARACTERÍSTICA',
    values='CANTIDAD',
    title=f"Distribución de ejemplares vivos y muertos en {estado_seleccionado}",
    labels={'CANTIDAD': 'Número de Incidencias'}
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True, key="grafico_pastel2")
########################################

#############################################

#########################################################
# Agrupar y contar incidencias por AÑO y CARACTERÍSTICA
df_grouped = df.groupby(["AÑO", "CARACTERÍSTICA"]).size().reset_index(name="INCIDENCIAS")


fig = px.bar(
    df_grouped,
    x="AÑO",
    y="INCIDENCIAS",
    color="CARACTERÍSTICA",
    barmode="group",
    title="Relación de ejemplares muertos-vivos registrados en cada año",
    labels={"INCIDENCIAS": "Número de Incidencias"}
)

# Mostrar la gráfica
st.plotly_chart(fig, use_container_width=True, key="grafico_1")
##########################################

st.header("CANTIDAD DE EJEMPLARES VIVOS Y MUERTOS")
##########################################
selected_status = st.selectbox("Selecciona el estado", ["Vivo", "Muerto"])

# Filtrar el DataFrame según la selección
df_filtered = (
    df[df["CARACTERÍSTICA"] == selected_status]
    .groupby(["Latitude", "Longitude", "SITIO", "ESTADO", "LOCALIDAD", "ID_SITIO"])
    .size()
    .reset_index(name="Count")
)

# Escalar el tamaño de los puntos
df_filtered["size"] = df_filtered["Count"] * 10

# Capa de Pydeck
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    id=f"{selected_status}-incidences",
    get_position=["Longitude", "Latitude"],
    get_color=[0, 128, 255] if selected_status == "Vivo" else [255, 0, 0],
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

# Estado de la vista del mapa
if not df_filtered.empty:
    view_state = pdk.ViewState(
        latitude=df_filtered["Latitude"].mean(),
        longitude=df_filtered["Longitude"].mean(),
        zoom=6,
        pitch=30,
        controller=True
    )
else:
    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=2)

# Tooltip que incluye "SITIO", "ESTADO", "LOCALIDAD" y "ID_SITIO"
tooltip = {
    "html": """
    <b>Coordenadas:</b> {Latitude}, {Longitude}<br>
    <b>Incidencias:</b> {Count}<br>

    <b>ID Sitio:</b> {ID_SITIO}<br>

    """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# Crear el mapa
chart = pdk.Deck(
    layers=[point_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

# Mostrar el mapa
st.pydeck_chart(chart)

################################################################################
st.header("CANTIDAD DE EJEMPLARES ADULTOS Y JUVENILES")
######################################################################
selected_status = st.selectbox("Selecciona el estado", ["Adulto", "Juvenil"])


df_filtered = (
    df[df["ESTADO ESTRUCTURAL"] == selected_status]
    .groupby(["Latitude", "Longitude"])
    .size()
    .reset_index(name="Count")
)


df_filtered["size"] = df_filtered["Count"] * 10


point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    id=f"{selected_status}-incidences",
    get_position=["Longitude", "Latitude"],
    get_color="[100, 200, 100]" if selected_status == "Adulto" else "[255, 165, 0]",  # Azul para "Adulto" y naranja para "Juvenil"
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

#estado inicial del mapa
view_state = pdk.ViewState(
    latitude=df_filtered["Latitude"].mean(),
    longitude=df_filtered["Longitude"].mean(),
    controller=True,
    zoom=6,
    pitch=30,
)


chart = pdk.Deck(
    point_layer,
    initial_view_state=view_state,
    tooltip={"text": "Coordenadas: {Latitude}, {Longitude}\nIncidencias: {Count}"},
)


event = st.pydeck_chart(chart, on_select="rerun", selection_mode="multi-object")


if event and event.selection:
    st.write(event.selection)

##########################################MAPA SIN FILTROS, MOSTRAR TODAS LAS COORDENADAS##################
st.header("CANTIDAD DE REGISTROS X ESTADO")

# Agrupar datos incluyendo la columna "ESPECIE" y "SITIO"
df_all = (
    df.groupby(["Latitude", "Longitude", "ID_SITIO", "ESTADO", "LOCALIDAD", "SITIO", "ESPECIE"])
    .size()
    .reset_index(name="Count")
)

# Escalar el tamaño de los puntos
df_all["size"] = df_all["Count"] * 10

# Capa de Pydeck
point_layer_all = pdk.Layer(
    "ScatterplotLayer",
    data=df_all,
    id="all-incidences",
    get_position=["Longitude", "Latitude"],
    get_color=[100, 200, 100],
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

# Estado de la vista del mapa
if not df_all.empty:
    view_state_all = pdk.ViewState(
        latitude=df_all["Latitude"].mean(),
        longitude=df_all["Longitude"].mean(),
        zoom=6,
        pitch=30,
        controller=True
    )
else:
    view_state_all = pdk.ViewState(latitude=0, longitude=0, zoom=2)

# Tooltip actualizado con la columna "ESPECIE" y "SITIO"
tooltip = {
    "html": """
    <b>Coordenadas:</b> {Latitude}, {Longitude}<br>
    <b>Incidencias:</b> {Count}<br>
    <b>Estado:</b> {ESTADO}<br>
    <b>Localidad:</b> {LOCALIDAD}<br>
    <b>Sitio:</b> {SITIO}<br>
    <b>ID_SITIO:</b> {ID_SITIO}<br>
    <b>Especie:</b> {ESPECIE}<br>
    """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# Crear el mapa
chart_all = pdk.Deck(
    layers=[point_layer_all],
    initial_view_state=view_state_all,
    tooltip=tooltip,
)

st.subheader("Mapa sin filtro (Muestra todas las coordenadas)")
st.pydeck_chart(chart_all)


#############################################################
###########################################################
st.header("Cantidad de ejemplares x condición (Conservado,Restaurado,etc.)")
selected_condition = st.selectbox(
    "Selecciona la condición",
    ["Conservado", "Restaurado", "Degradado", "Degradado con árboles muertos en Pie"],
    key="selectbox_condicion"
)

# Filtrar el DataFrame según la selección
df_filtered = (
    df[df["CONDICIÓN"] == selected_condition]
    .groupby(["Latitude", "Longitude", "SITIO", "ESTADO", "LOCALIDAD", "ID_SITIO"])
    .size()
    .reset_index(name="Count")
)

# Escalar el tamaño de los puntos
df_filtered["size"] = df_filtered["Count"] * 10

# Asignar colores distintos según la condición seleccionada
color_map = {
    "Conservado": [34, 139, 34],  # Verde
    "Restaurado": [30, 144, 255],  # Azul
    "Degradado": [255, 165, 0],  # Naranja
    "Degradado con árboles muertos en Pie": [255, 69, 0]  # Rojo
}

# Capa de Pydeck
point_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_filtered,
    id=f"{selected_condition}-incidences",
    get_position=["Longitude", "Latitude"],
    get_color=color_map.get(selected_condition, [100, 100, 100]),
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)

# Estado de la vista del mapa
if not df_filtered.empty:
    view_state = pdk.ViewState(
        latitude=df_filtered["Latitude"].mean(),
        longitude=df_filtered["Longitude"].mean(),
        zoom=6,
        pitch=30,
        controller=True
    )
else:
    view_state = pdk.ViewState(latitude=0, longitude=0, zoom=2)

# Tooltip que incluye "SITIO", "ESTADO", "LOCALIDAD" y "ID_SITIO"
tooltip = {
    "html": """
    <b>Coordenadas:</b> {Latitude}, {Longitude}<br>
    <b>Incidencias:</b> {Count}<br>
    <b>Sitio:</b> {SITIO}<br>
    <b>Estado:</b> {ESTADO}<br>
    <b>Localidad:</b> {LOCALIDAD}<br>
    <b>ID Sitio:</b> {ID_SITIO}<br>
    """,
    "style": {"backgroundColor": "steelblue", "color": "white"}
}

# Crear el mapa
chart = pdk.Deck(
    layers=[point_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
)

# Mostrar el mapa


st.pydeck_chart(chart)