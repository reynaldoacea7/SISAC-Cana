import streamlit as st
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
