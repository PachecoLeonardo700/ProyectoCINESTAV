

import streamlit as st
import pandas as pd
import plotly.express as px
import pydeck as pdk



df = pd.read_excel("datos/dfDatosFinales2.xlsx")
st.header("ANÁLISIS DE MANGLARES EN LA ZONA SUR DE MÉXICO")
###################################################################
# Lista de estados posibles
estados_posibles = ['Yucatan', 'Campeche', 'Quintana Roo', 'Tamaulipas', 'Chiapas', 'Oaxaca']


estado_seleccionado = st.selectbox("Selecciona un estado", estados_posibles)


df_filtrado = df[df['ESTADO'] == estado_seleccionado]

# Agrupar por especie y contar las incidencias
df_especies = df_filtrado['ESPECIE'].value_counts().reset_index(name='CANTIDAD')
df_especies.columns = ['ESPECIE', 'CANTIDAD']

# Crear el gráfico de pastel
fig = px.pie(
    df_especies,
    names='ESPECIE',
    values='CANTIDAD',
    title=f"Distribución de Especies en {estado_seleccionado}",
    labels={'CANTIDAD': 'Número de Ejemplares'}
)

# Mostrar la gráfica
st.plotly_chart(fig, use_container_width=True, key="grafico_pastel")
########################################
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


df_filtered = (
    df[df["CARACTERÍSTICA"] == selected_status]
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
    get_color="[0, 128, 255]" if selected_status == "Vivo" else "[255, 0, 0]",  # Azul para "Vivo" y rojo para "Muerto"
    pickable=True,
    auto_highlight=True,
    get_radius="size",
)


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