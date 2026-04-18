import streamlit as st
import pandas as pd
import numpy as np

def mostrar_diagnostico():
    st.title("🔍 Diagnóstico de Labranza")
    st.markdown("Ingrese los parámetros del suelo y cultivo")
    
    with st.form("diagnostico_form"):
        materia_organica = st.number_input("Materia Orgánica (%)", 0.0, 10.0, 2.5)
        densidad_aparente = st.number_input("Densidad Aparente (g/cm³)", 0.5, 2.0, 1.3)
        resistencia = st.number_input("Resistencia a la Penetración (MPa)", 0.0, 5.0, 2.0)
        submitted = st.form_submit_button("Evaluar")
        
        if submitted:
            # Lógica simple de umbrales
            if materia_organica < 2.0:
                st.warning("Materia orgánica baja. Recomendado: labranza reducida con cobertura.")
            elif densidad_aparente > 1.4:
                st.warning("Densidad alta. Considere descompactación mecánica.")
            else:
                st.success("Parámetros dentro de rangos aceptables.")
            st.info("Variante sugerida: Labranza Cero + Rotación de cultivos.")
