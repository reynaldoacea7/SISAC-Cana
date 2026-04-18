import streamlit as st
import numpy as np
import plotly.express as px

def mostrar_simulacion():
    st.title("⚙️ Simulación de Rendimiento")
    st.markdown("Simule el rendimiento de la caña según parámetros de labranza")
    
    n = st.slider("Número de simulaciones", 100, 10000, 1000)
    rendimiento_base = np.random.normal(80, 10, n)  # t/ha
    fig = px.histogram(rendimiento_base, nbins=30, title="Distribución de Rendimiento Simulado")
    st.plotly_chart(fig)
