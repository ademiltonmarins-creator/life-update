import streamlit as st
from database import c

def historico():
    st.subheader("📜 Histórico do Jogador")

    dados = c.execute("""
        SELECT tipo, descricao, data
        FROM historico
        WHERE user_id=?
        ORDER BY id DESC
    """, (st.session_state.user_id,)).fetchall()

    if not dados:
        st.info("Nenhum registro ainda.")
        return

    for h in dados:
        st.write(f"🗂 {h[2]} — [{h[0].upper()}] {h[1]}")