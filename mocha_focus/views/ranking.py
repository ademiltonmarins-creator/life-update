import streamlit as st
from database import c
from config import MASTER_USER

def ranking():
    st.subheader("🏆 Ranking de Jogadores")

    dados = c.execute("""
        SELECT username, xp
        FROM users
        WHERE username != ?
        ORDER BY xp DESC
    """, (MASTER_USER,)).fetchall()

    if not dados:
        st.info("Nenhum jogador encontrado.")
        return

    for pos, jogador in enumerate(dados, start=1):
        st.write(f"{pos}º — {jogador[0]} ({jogador[1]} XP)")