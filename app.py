import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Definir los procesos agrupados por artículos de los estatutos con referencias corregidas
procesos = [
    ("Inicio", "Convocatoria elecciones", "Convocatoria electoral", 0, "convocatoria"),
    ("Artículo 32", "Junta Electoral", "Constitución Junta Electoral", 3, "convocatoria"),
    ("Artículo 36", "Publicidad Censo Electoral", "Publicidad y aprobación censo", 8, "convocatoria"),
    ("Artículo 39", "Candidaturas", "Presentación y resolución de candidaturas", 20, "convocatoria"),
    ("Artículo 41", "Campaña Electoral", "Duración de la campaña", 10, "candidaturas firmes"),
    ("Artículo 42", "Voto por Correo", "Solicitud y envío de voto", 25, "convocatoria"),
    ("Jornada Electoral", "Elecciones", "Día de la elección", 0, "elecciones"),
    ("Artículo 45", "Interventores", "Plazo para nombramiento", -3, "elecciones"),
    ("Artículo 46", "Apoderados", "Plazo para nombramiento", -5, "elecciones"),
    ("Artículo 49", "Proclamación de Electos", "Proclamación y recursos", 1, "elecciones"),
    ("Artículo 50", "Nombramiento Junta Rectora", "Constitución Junta Rectora", 15, "elecciones"),
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
    for articulo, proceso, descripcion, dias, referencia in procesos:
        if referencia == "convocatoria":
            fecha_referencia = fecha_convocatoria
            descripcion_referencia = "Fecha de convocatoria"
        elif referencia == "elecciones":
            fecha_referencia = fecha_elecciones
            descripcion_referencia = "Fecha de elecciones"
        elif referencia == "candidaturas firmes":
            fecha_referencia = fecha_convocatoria + timedelta(days=20 + 2 + 2)  # Tras resolución de recursos
            descripcion_referencia = "Fecha de candidaturas firmes"
        
        fecha_inicio = fecha_referencia
        fecha_fin = fecha_referencia + timedelta(days=dias)
        dia_semana = fecha_fin.strftime("%A")
        dia_semana_esp = {"Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles", "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"}.get(dia_semana, dia_semana)
        
        # Destacar la jornada electoral en rojo si cae en sábado o domingo
        destacar = "Sí" if proceso == "Elecciones" and dia_semana in ["Saturday", "Sunday"] else "No"
        
        datos.append([
            articulo, proceso, descripcion, dias, fecha_referencia.strftime("%d/%m/%Y"),
            descripcion_referencia, fecha_inicio.strftime("%d/%m/%Y"), fecha_fin.strftime("%d/%m/%Y"), dia_semana_esp, destacar
        ])
    
    return pd.DataFrame(datos, columns=[
        "Artículo", "Proceso", "Descripción", "Días de Plazo", "Fecha de Referencia", "Descripción Fecha Referencia",
        "Inicio del Plazo", "Fin del Plazo", "Día de la Semana", "Destacar"
    ])

# Interfaz en Streamlit
st.title("Calculadora de Calendario Electoral")

modo = st.radio("Selecciona cómo calcular el calendario:", ("Desde la fecha de convocatoria", "Desde la fecha de elecciones"))

if modo == "Desde la fecha de convocatoria":
    fecha_convocatoria = st.date_input("Selecciona la fecha de convocatoria:", datetime.today())
    calendario = calcular_calendario(fecha_convocatoria=fecha_convocatoria)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario)
else:
    fecha_elecciones = st.date_input("Selecciona la fecha de elecciones:", datetime.today())
    calendario = calcular_calendario(fecha_elecciones=fecha_elecciones)
    if calendario is not None:
        st.write("### Calendario Electoral Calculado:")
        st.dataframe(calendario)

if calendario is None:
    st.warning("Selecciona una fecha para calcular el calendario.")
