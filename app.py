import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Definir los hitos y sus plazos en días
hitos = [
    ("Constitución Junta Electoral", 3),
    ("Publicidad Censo Provisional", 1),
    ("Fin Publicidad Censo Provisional", 8),
    ("Plazo Recurso Censo Provisional", 8),
    ("Resolución Recursos Censo", 2),
    ("Aprobación Censo Definitivo", 1),
    ("Inicio Presentación Candidaturas", 20),
    ("Fin Presentación Candidaturas", 10),
    ("Rectificación y Publicación Candidaturas", 3),
    ("Presentación Recursos Candidaturas", 2),
    ("Resolución Recursos Candidaturas", 2),
    ("Inicio Campaña Electoral", 8),
    ("Duración Campaña Electoral", 10),
    ("Sorteo Mesas Electorales", 13),
    ("Plazo Excusas Miembros Mesa", 2),
    ("Resolución Excusas Miembros Mesa", 3),
    ("Plazo Nombramiento Interventores", -3),
    ("Plazo Nombramiento Apoderados", -5),
    ("Proclamación de Electos", 1),
    ("Recurso Proclamación Electos", 3),
    ("Resolución Recurso Electos", 3),
    ("Constitución Junta Rectora", 15),
]

def calcular_calendario(fecha_convocatoria=None, fecha_elecciones=None):
    if fecha_elecciones:
        fecha_convocatoria = fecha_elecciones - timedelta(days=69)  # Retroceder el mínimo tiempo del proceso
    elif not fecha_convocatoria:
        return None
    
    fechas = [("Fecha Convocatoria", fecha_convocatoria.strftime("%d/%m/%Y"))]
    fecha_actual = fecha_convocatoria
    
    for evento, dias in hitos:
        fecha_actual = fecha_convocatoria + timedelta(days=dias)
        fechas.append((evento, fecha_actual.strftime("%d/%m/%Y")))
    
    return pd.DataFrame(fechas, columns=["Evento", "Fecha"])

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
