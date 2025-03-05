import streamlit as st
import pandas as pd
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
        fecha_convocatoria = fecha_elecciones - timedelta(days=69)  # Retroceder el mínimo tiempo del proceso
    elif not fecha_convocatoria:
        return None
    
    datos = []
    fecha_actual = fecha_convocatoria
    
    for evento, articulo, dias in hitos:
        fecha_inicio = fecha_actual
        fecha_actual = fecha_convocatoria + timedelta(days=dias)
        fecha_fin = fecha_actual
        dia_semana = fecha_fin.strftime("%A")
        datos.append([evento, articulo, dias, fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"), dia_semana])
    
    return pd.DataFrame(datos, columns=["Hito", "Artículo Estatutos", "Días de Plazo", "Inicio del Plazo", "Fin del Plazo", "Día de la Semana"])

# Interfaz en Streamlit
st.title("Calculadora de Calendario Electoral")

# Opción de elegir fecha de convocatoria o elecciones
modo = st.radio("Selecciona cómo calcular el calendario:", ("Desde la fecha de convocatoria", "Desde la fecha de elecciones"))

if modo == "Desde la fecha de convocatoria":
    fecha_convocatoria = st.date_input("Selecciona la fecha de convocatoria:", datetime.today())
    calendario = calcular_calendario(fecha_convocatoria=fecha_convocatoria)
else:
    fecha_elecciones = st.date_input("Selecciona la fecha de elecciones:", datetime.today())
    calendario = calcular_calendario(fecha_elecciones=fecha_elecciones)

if calendario is not None:
    st.write("### Calendario Electoral Calculado:")
    st.dataframe(calendario)
else:
    st.warning("Selecciona una fecha para calcular el calendario.")
