import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Definir los procesos agrupados por artículos de los estatutos con referencias corregidas
procesos = [
    ("Inicio", "Convocatoria elecciones", "Convocatoria electoral", 0, "convocatoria"),
    ("Artículo 32", "Junta Electoral", "Constitución Junta Electoral", 3, "convocatoria"),
    ("Artículo 36", "Publicidad Censo Electoral", "Publicidad y aprobación censo", 8, "convocatoria"),
    ("Artículo 36", "Plazo Recursos Censo", "Plazo de recursos sobre el censo", 8, "convocatoria"),
    ("Artículo 36", "Resolución Recursos Censo", "Resolución de recursos sobre el censo", 2, "censo recursos"),
    ("Artículo 39", "Candidaturas", "Presentación y resolución de candidaturas", 10, "convocatoria"),
    ("Artículo 39", "Rectificación Candidaturas", "Corrección de errores y publicación", 3, "candidaturas"),
    ("Artículo 39", "Plazo Recursos Candidaturas", "Plazo para interponer recursos", 2, "candidaturas"),
    ("Artículo 39", "Resolución Recursos Candidaturas", "Resolución de recursos sobre candidaturas", 2, "candidaturas recursos"),
    ("Artículo 41", "Campaña Electoral", "Duración de la campaña", 10, "candidaturas firmes"),
    ("Artículo 42", "Voto por Correo", "Solicitud y envío de voto", 25, "convocatoria"),
    ("Artículo 44", "Sorteo Mesas", "Sorteo y notificación de miembros de mesas", 13, "convocatoria"),
    ("Artículo 44", "Plazo Excusas Mesas", "Plazo de presentación de excusas", 2, "sorteo mesas"),
    ("Artículo 44", "Resolución Excusas Mesas", "Resolución de excusas presentadas", 3, "excusas mesas"),
    ("Jornada Electoral", "Elecciones", "Día de la elección", 0, "elecciones"),
    ("Artículo 45", "Interventores", "Plazo para nombramiento", -3, "elecciones"),
    ("Artículo 46", "Apoderados", "Plazo para nombramiento", -5, "elecciones"),
    ("Artículo 48", "Escrutinio", "Recepción de actas y escrutinio", 1, "elecciones"),
    ("Artículo 49", "Proclamación de Electos", "Proclamación de vocales electos", 1, "elecciones"),
    ("Artículo 49", "Plazo Recursos Electos", "Plazo de interposición de recursos", 3, "proclamación electos"),
    ("Artículo 49", "Resolución Recursos Electos", "Resolución de recursos sobre electos", 3, "recursos electos"),
    ("Artículo 50", "Nombramiento Junta Rectora", "Constitución Junta Rectora", 15, "elecciones"),
]

def calcular_calendario(fecha_convocatoria=None, fecha_elecciones=None):
    if fecha_elecciones:
        fecha_convocatoria = fecha_elecciones - timedelta(days=20)
    elif fecha_convocatoria:
        fecha_elecciones = fecha_convocatoria + timedelta(days=20)
    else:
        return None
    
    fechas_referencia = {
        "convocatoria": fecha_convocatoria,
        "elecciones": fecha_elecciones,
    }
    
    datos = []
    for articulo, proceso, descripcion, dias, referencia in procesos:
        if referencia not in fechas_referencia:
            fechas_referencia[referencia] = fechas_referencia.get("convocatoria", fecha_convocatoria) + timedelta(days=dias)
        
        fecha_referencia = fechas_referencia[referencia]
        fecha_inicio = fecha_referencia
        fecha_fin = fecha_referencia + timedelta(days=dias)
        dia_semana = fecha_fin.strftime("%A")
        dia_semana_esp = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}.get(dia_semana, dia_semana)
        
        datos.append([
            articulo, proceso, descripcion, dias, fecha_referencia.strftime("%d/%m/%Y"),
            fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"), dia_semana_esp
        ])
    
    return pd.DataFrame(datos, columns=[
        "Artículo", "Proceso", "Descripción", "Días de Plazo", "Fecha de Referencia",
        "Inicio del Plazo", "Fin del Plazo", "Día de la Semana"
    ])

# Interfaz en Streamlit
st.title("Calculadora de Calendario Electoral")

modo = st.radio("Selecciona cómo calcular el calendario:", ("Desde la fecha de convocatoria", "Desde la fecha de elecciones"))

if modo == "Desde la fecha de convocatoria":
    fecha_convocatoria = st.date_input("Selecciona la fecha de convocatoria:", datetime.today())
    calendario = calcular_calendario(fecha_convocatoria=fecha_convocatoria)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario, use_container_width=True)
else:
    fecha_elecciones = st.date_input("Selecciona la fecha de elecciones:", datetime.today())
    calendario = calcular_calendario(fecha_elecciones=fecha_elecciones)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario, use_container_width=True)

if calendario is None:
    st.warning("Selecciona una fecha para calcular el calendario.")
