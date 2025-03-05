import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

# Definir los procesos agrupados por artículos de los estatutos
procesos = [
    ("Artículo 32", "Junta Electoral", "Constitución Junta Electoral", 3),
    ("Artículo 36", "Publicidad Censo Electoral", "Publicidad y aprobación censo", 8),
    ("Artículo 39", "Candidaturas", "Presentación y resolución de candidaturas", 20),
    ("Artículo 41", "Campaña Electoral", "Duración de la campaña", 10),
    ("Artículo 42", "Voto por Correo", "Solicitud y envío de voto", 25),
    ("Artículo 44", "Jornada Electoral y Mesas", "Sorteo y gestión de mesas", 13),
    ("Artículo 45", "Interventores", "Plazo para nombramiento", -3),
    ("Artículo 46", "Apoderados", "Plazo para nombramiento", -5),
    ("Artículo 49", "Proclamación de Electos", "Proclamación y recursos", 3),
    ("Artículo 50", "Nombramiento Junta Rectora", "Constitución Junta Rectora", 15),
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
    for articulo, proceso, descripcion, dias in procesos:
        fecha_inicio = fecha_convocatoria
        fecha_fin = fecha_convocatoria + timedelta(days=dias)
        dia_semana = fecha_fin.strftime("%A")
        datos.append([articulo, proceso, descripcion, dias, fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"), dia_semana])
    
    return pd.DataFrame(datos, columns=["Artículo", "Proceso", "Descripción", "Días de Plazo", "Inicio del Plazo", "Fin del Plazo", "Día de la Semana"])

def generar_gantt(calendario):
    calendario["Inicio del Plazo"] = pd.to_datetime(calendario["Inicio del Plazo"], format="%d/%m/%Y")
    calendario["Fin del Plazo"] = pd.to_datetime(calendario["Fin del Plazo"], format="%d/%m/%Y")
    
    gantt_chart = alt.Chart(calendario).mark_bar().encode(
        x=alt.X("Inicio del Plazo:T", title="Fecha de Inicio"),
        x2=alt.X2("Fin del Plazo:T"),
        y=alt.Y("Proceso:N", title="Procesos"),
        color=alt.Color("Artículo:N", title="Artículo", scale=alt.Scale(scheme="category20"))
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
