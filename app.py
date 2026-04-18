import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="SISAC-Caña",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="auto"
)

# Cargar configuración
@st.cache_resource
def load_config():
    with open("config_app.json", "r") as f:
        return json.load(f)

config = load_config()

# Inicializar estado de sesión
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Sidebar con logo y navegación
with st.sidebar:
    if os.path.exists(config["logo_path"]):
        st.image(config["logo_path"], width=200)
    else:
        st.warning("Logo no encontrado")
    
    st.markdown("## 📌 Navegación")
    opcion = st.radio(
        "Ir a:",
        ["🏠 Inicio", "🔍 Diagnóstico", "📊 Análisis Estadístico", 
         "📈 Análisis DEA", "⚙️ Simulación", "👥 Gestión de Usuarios"]
    )

# Página principal
if not st.session_state.authenticated:
    st.title("🔐 Inicio de Sesión")
    from login_html import mostrar_login
    mostrar_login()
else:
    if opcion == "🏠 Inicio":
        st.title("🌾 SISAC-Caña")
        st.markdown("**Sistema de Selección de Variantes de Labranza en Caña de Azúcar**")
        st.markdown("Bajo principios de **Agricultura de Conservación**")
        if os.path.exists(config["map_path"]):
            st.image(config["map_path"], caption="Mapa de Cienfuegos")
    
    elif opcion == "🔍 Diagnóstico":
        from modulos.diagnostico import mostrar_diagnostico
        mostrar_diagnostico()
    
    elif opcion == "📊 Análisis Estadístico":
        from modulos.analisis_estadistico import mostrar_analisis_estadistico
        mostrar_analisis_estadistico()
    
    elif opcion == "📈 Análisis DEA":
        from modulos.analisis_dea import mostrar_analisis_dea
        mostrar_analisis_dea()
    
    elif opcion == "⚙️ Simulación":
        from modulos.simulacion import mostrar_simulacion
        mostrar_simulacion()
    
    elif opcion == "👥 Gestión de Usuarios":
        from modulos.gestion_usuarios import mostrar_gestion_usuarios
        mostrar_gestion_usuarios()
