import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Definir los hitos con sus plazos en días y sus artículos en los estatutos
hitos = [
    ("Constitución Junta Electoral", "Artículo 32", 3),
    ("Publicidad Censo Provisional", "Artículo 36", 1),
    ("Fin Publicidad Censo Provisional", "Artículo 36", 8),
    ("Plazo Recurso Censo Provisional", "Artículo 36", 8),
    ("Resolución Recursos Censo", "Artículo 36", 2),
    ("Aprobación Censo Definitivo", "Artículo 36", 1),
    ("Inicio Presentación Candidaturas", "Artículo 39", 20),
    ("Fin Presentación Candidaturas", "Artículo 39", 10),
    ("Rectificación y Publicación Candidaturas", "Artículo 39", 3),
    ("Presentación Recursos Candidaturas", "Artículo 39", 2),
    ("Resolución Recursos Candidaturas", "Artículo 39", 2),
    ("Inicio Campaña Electoral", "Artículo 41", 8),
    ("Duración Campaña Electoral", "Artículo 41", 10),
    ("Sorteo Mesas Electorales", "Artículo 44", 13),
    ("Plazo Excusas Miembros Mesa", "Artículo 44", 2),
    ("Resolución Excusas Miembros Mesa", "Artículo 44", 3),
    ("Plazo Nombramiento Interventores", "Artículo 45", -3),
    ("Plazo Nombramiento Apoderados", "Artículo 46", -5),
    ("Proclamación de Electos", "Artículo 49", 1),
    ("Recurso Proclamación Electos", "Artículo 49", 3),
    ("Resolución Recurso Electos", "Artículo 49", 3),
    ("Constitución Junta Rectora", "Artículo 50", 15),
]

def calcular_calendario(fecha_convocatoria=None, fecha_elecciones=None):
    if fecha_elecciones:
        fecha_convocatoria = fecha_elecciones - timedelta(days=20)
        st.write(f"**Fecha de Convocatoria Calculada:** {fecha_convocatoria.strftime('%d/%m/%Y')}")
    elif fecha_convocatoria:
        fecha_elecciones = fecha_convocatoria + timedelta(days=20)
        st.write(f"**Fecha de Elecciones Calculada:** {fecha_elecciones.strftime('%d/%m/%Y')}")
    else:
        return None
    
    datos = []
    for evento, articulo, dias in hitos:
        fecha_inicio = fecha_convocatoria
        fecha_fin = fecha_convocatoria + timedelta(days=dias)
        dia_semana = fecha_fin.strftime("%A")
        datos.append([evento, articulo, dias, fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"), dia_semana])
    
    return pd.DataFrame(datos, columns=["Hito", "Artículo Estatutos", "Días de Plazo", "Inicio del Plazo", "Fin del Plazo", "Día de la Semana"])

def generar_gantt(calendario):
    calendario["Inicio del Plazo"] = pd.to_datetime(calendario["Inicio del Plazo"], format="%d/%m/%Y")
    calendario["Fin del Plazo"] = pd.to_datetime(calendario["Fin del Plazo"], format="%d/%m/%Y")
    
    gantt_chart = alt.Chart(calendario).mark_bar().encode(
        x=alt.X("Inicio del Plazo:T", title="Fecha de Inicio"),
        x2=alt.X2("Fin del Plazo:T"),
        y=alt.Y("Hito:N", title="Hitos"),
        color=alt.value("steelblue")
    ).properties(title="Diagrama de Gantt del Calendario Electoral", width=800, height=600)
    
    st.altair_chart(gantt_chart)

# Interfaz en Streamlit
st.title("Calculadora de Calendario Electoral")

modo = st.radio("Selecciona cómo calcular el calendario:", ("Desde la fecha de convocatoria", "Desde la fecha de elecciones"))

if modo == "Desde la fecha de convocatoria":
    fecha_convocatoria = st.date_input("Selecciona la fecha de convocatoria:", datetime.today())
    calendario = calcular_calendario(fecha_convocatoria=fecha_convocatoria)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario)
        generar_gantt(calendario)
else:
    fecha_elecciones = st.date_input("Selecciona la fecha de elecciones:", datetime.today())
    calendario = calcular_calendario(fecha_elecciones=fecha_elecciones)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario)
        generar_gantt(calendario)

if calendario is None:
    st.warning("Selecciona una fecha para calcular el calendario.")
