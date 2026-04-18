import streamlit as st
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
