import streamlit as st
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
