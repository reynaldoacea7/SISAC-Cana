import os
import shutil

# Ruta base donde se creará el proyecto
BASE_DIR = r"F:\SISAC-Caña APK"

# Estructura de carpetas
folders = [
    "data",
    "logs",
    "assets/images",
    "modulos",
    "utils"
]

# Archivos con su contenido
files = {}

# 1. requirements.txt
files["requirements.txt"] = """streamlit==1.29.0
pandas==2.0.3
statsmodels==0.14.0
scipy==1.11.4
plotly==5.17.0
matplotlib==3.7.2
pulp==2.7.0
bcrypt==4.0.1
openpyxl==3.1.2
numpy==1.24.3
"""

# 2. config_app.json
files["config_app.json"] = """{
    "database_path": "data/sisac.db",
    "logo_path": "assets/images/logo_sisac.png",
    "map_path": "assets/images/cienfuegos_map.jpg",
    "umbrales_por_defecto": {
        "materia_organica": 2.5,
        "densidad_aparente": 1.3,
        "resistencia_penetracion": 2.0
    },
    "modo_oscuro": true,
    "auditoria_activa": true
}
"""

# 3. app.py (archivo principal de Streamlit)
files["app.py"] = """import streamlit as st
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
"""

# 4. login_html.py (para mostrar login embebido)
files["login_html.py"] = """import streamlit as st
import bcrypt
import sqlite3
import pandas as pd

def mostrar_login():
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Ingresar")
        
        if submitted:
            # Aquí validar contra base de datos
            # Por simplicidad, usuario demo: admin / admin123
            if username == "admin" and password == "admin123":
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Credenciales incorrectas")
"""

# 5. login.html (por si se usa incrustación directa)
files["login.html"] = """<!DOCTYPE html>
<html>
<head>
    <title>SISAC-Caña Login</title>
    <link rel="stylesheet" href="assets/login_style.css">
</head>
<body>
    <div class="login-container">
        <img src="assets/images/logo_sisac.png" alt="Logo" width="150">
        <h2>Iniciar Sesión</h2>
        <input type="text" id="username" placeholder="Usuario">
        <input type="password" id="password" placeholder="Contraseña">
        <button onclick="login()">Entrar</button>
    </div>
    <script>
        function login() {
            alert("Esta página es solo referencia. Use la interfaz de Streamlit.");
        }
    </script>
</body>
</html>
"""

# 6. assets/login_style.css
files["assets/login_style.css"] = """body {
    background-color: #1e1e2f;
    font-family: Arial, sans-serif;
}
.login-container {
    width: 300px;
    margin: 100px auto;
    padding: 20px;
    background: white;
    border-radius: 10px;
    text-align: center;
}
input, button {
    display: block;
    width: 90%;
    margin: 10px auto;
    padding: 8px;
}
button {
    background-color: #4CAF50;
    color: white;
    border: none;
    cursor: pointer;
}
"""

# 7. Módulo diagnóstico
files["modulos/diagnostico.py"] = """import streamlit as st
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
"""

# 8. Módulo análisis estadístico
files["modulos/analisis_estadistico.py"] = """import streamlit as st
import pandas as pd
import statsmodels.api as sm
from scipy import stats

def mostrar_analisis_estadistico():
    st.title("📊 Análisis Estadístico")
    st.markdown("Cargue un archivo CSV/Excel para ANOVA o Regresión")
    
    uploaded = st.file_uploader("Subir archivo", type=["csv", "xlsx"])
    if uploaded:
        df = pd.read_csv(uploaded) if uploaded.name.endswith('.csv') else pd.read_excel(uploaded)
        st.dataframe(df.head())
        
        # Selección de columnas
        num_cols = df.select_dtypes(include='number').columns.tolist()
        if len(num_cols) >= 2:
            y_col = st.selectbox("Variable dependiente (Y)", num_cols)
            x_cols = st.multiselect("Variables independientes (X)", [c for c in num_cols if c != y_col])
            if st.button("Ejecutar Regresión"):
                X = df[x_cols]
                X = sm.add_constant(X)
                y = df[y_col]
                model = sm.OLS(y, X).fit()
                st.write(model.summary())
"""

# 9. Módulo DEA
files["modulos/analisis_dea.py"] = """import streamlit as st
import pandas as pd
from pulp import *
import numpy as np

def mostrar_analisis_dea():
    st.title("📈 Análisis Envolvente de Datos (DEA)")
    st.markdown("Calcule la eficiencia técnica de unidades productivas")
    
    uploaded = st.file_uploader("Cargar datos (CSV con inputs y outputs)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df)
        # Aquí se implementaría el modelo DEA (simplificado)
        st.info("Módulo DEA en desarrollo. Próximamente disponible.")
"""

# 10. Módulo simulación
files["modulos/simulacion.py"] = """import streamlit as st
import numpy as np
import plotly.express as px

def mostrar_simulacion():
    st.title("⚙️ Simulación de Rendimiento")
    st.markdown("Simule el rendimiento de la caña según parámetros de labranza")
    
    n = st.slider("Número de simulaciones", 100, 10000, 1000)
    rendimiento_base = np.random.normal(80, 10, n)  # t/ha
    fig = px.histogram(rendimiento_base, nbins=30, title="Distribución de Rendimiento Simulado")
    st.plotly_chart(fig)
"""

# 11. Módulo gestión usuarios
files["modulos/gestion_usuarios.py"] = """import streamlit as st
import sqlite3
import bcrypt

def mostrar_gestion_usuarios():
    st.title("👥 Gestión de Usuarios")
    if st.session_state.get("username") != "admin":
        st.warning("Solo el administrador puede acceder.")
        return
    
    st.subheader("Lista de usuarios")
    conn = sqlite3.connect("data/sisac.db")
    df = pd.read_sql_query("SELECT username, role FROM users", conn)
    st.dataframe(df)
    conn.close()
    
    with st.expander("Agregar nuevo usuario"):
        new_user = st.text_input("Usuario")
        new_pass = st.text_input("Contraseña", type="password")
        role = st.selectbox("Rol", ["analista", "admin"])
        if st.button("Crear"):
            hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
            conn = sqlite3.connect("data/sisac.db")
            conn.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)", 
                         (new_user, hashed, role))
            conn.commit()
            conn.close()
            st.success("Usuario creado")
"""

# 12. Utilidades
files["utils/db_manager.py"] = """import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path("data/sisac.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            accion TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_audit(usuario, accion):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO auditoria (usuario, accion) VALUES (?,?)", (usuario, accion))
    conn.commit()
    conn.close()
"""

files["utils/dea_model.py"] = """# Modelo DEA (CCR, BCC) - por implementar
def calcular_eficiencia(inputs, outputs, rendimientos='constantes'):
    # Placeholder
    return [1.0] * len(inputs)
"""

files["utils/umbrales.py"] = """UMBRALES = {
    'materia_organica': {'min': 2.0, 'max': 5.0},
    'densidad_aparente': {'min': 1.0, 'max': 1.4},
    'resistencia_penetracion': {'min': 0.5, 'max': 2.5}
}
"""

files["utils/export_utils.py"] = """import pandas as pd
import streamlit as st
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def descargar_excel(df, nombre_archivo):
    st.download_button("📥 Descargar Excel", data=to_excel(df), file_name=nombre_archivo)
"""

# 13. Archivos de imagen placeholder (avisar al usuario)
# No podemos generar imágenes reales, pero creamos archivos .txt de aviso
files["assets/images/logo_sisac.txt"] = "COLOCA AQUÍ TU LOGO (logo_sisac.png) - Elimina este archivo y agrega la imagen real"
files["assets/images/cienfuegos_map.txt"] = "COLOCA AQUÍ EL MAPA (cienfuegos_map.jpg) - Elimina este archivo y agrega la imagen real"

# 14. Base de datos inicial (crear archivo .db vacío, pero se generará al ejecutar app.py)
# Crearemos un script init_db.py opcional
files["init_db.py"] = """from utils.db_manager import init_db
if __name__ == "__main__":
    init_db()
    print("Base de datos inicializada correctamente.")
"""

# 15. .gitignore
files[".gitignore"] = """__pycache__/
*.pyc
*.db
logs/
*.log
.env
venv/
"""

# Función para escribir archivos y carpetas
def create_project():
    # Crear carpetas
    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)
    
    # Crear archivos
    for filepath, content in files.items():
        full_path = os.path.join(BASE_DIR, filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✓ Creado: {full_path}")
    
    # Crear base de datos vacía (opcional)
    db_path = os.path.join(BASE_DIR, "data", "sisac.db")
    if not os.path.exists(db_path):
        open(db_path, "w").close()
        print(f"✓ Creado archivo BD vacío: {db_path}")
    
    print("\n✅ Proyecto SISAC-Caña generado exitosamente en:", BASE_DIR)
    print("🔧 Próximos pasos:")
    print("1. Reemplaza los archivos de imagen en assets/images/ con tus propios archivos .png y .jpg")
    print("2. Ejecuta 'python init_db.py' para crear las tablas de la base de datos")
    print("3. Ejecuta 'streamlit run app.py' para probar localmente")
    print("4. Sigue las instrucciones de despliegue en la nube (Streamlit Cloud o Railway)")

if __name__ == "__main__":
    create_project()