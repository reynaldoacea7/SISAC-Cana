import pandas as pd
import streamlit as st
from io import BytesIO

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

def descargar_excel(df, nombre_archivo):
    st.download_button("📥 Descargar Excel", data=to_excel(df), file_name=nombre_archivo)
