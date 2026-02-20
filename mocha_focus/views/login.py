import streamlit as st
from database import c, conn
from utils import atualizar_avatar_por_nivel

def login():
    st.title("Life Update RPG")

    user = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Login"):
        u = c.execute("""SELECT * FROM users
            WHERE username=? AND password=?""",
            (user,senha)).fetchone()

        if u:
            st.session_state.user_id = u[0]
            atualizar_avatar_por_nivel(u[0])
            st.rerun()
        else:
            st.error("Usuário inválido")

    st.divider()

    novo = st.text_input("Novo usuário")
    nova = st.text_input("Nova senha",
                         type="password")

    if st.button("Cadastrar"):
        try:
            c.execute("""INSERT INTO users
                (username,password)
                VALUES (?,?)""",
                (novo,nova))
            conn.commit()
            st.success("Conta criada")
        except:
            st.error("Usuário já existe")