import streamlit as st
from database import c, conn
from utils import atualizar_nivel, registrar
from config import MASTER_USER

def metas():
    st.subheader("🎯 Metas Globais")

    username = c.execute(
        "SELECT username FROM users WHERE id=?",
        (st.session_state.user_id,)
    ).fetchone()[0]

    # ===== ADMIN CRIA META =====
    if username == MASTER_USER:
        st.subheader("Criar Nova Meta")

        titulo = st.text_input("Título da Meta")
        desc = st.text_area("Descrição")
        xp = st.number_input("XP recompensa", 10, 500, 50)
        core = st.number_input("Core recompensa", 5, 200, 20)

        if st.button("Criar Meta"):
            c.execute("""
                INSERT INTO metas
                (titulo, descricao, xp, core)
                VALUES (?,?,?,?)
            """, (titulo, desc, xp, core))
            conn.commit()
            st.success("Meta criada!")
            st.rerun()

        st.divider()

    # ===== LISTAR METAS =====
    dados = c.execute("""
        SELECT id, titulo, descricao, xp, core
        FROM metas
        WHERE ativa=1
    """).fetchall()

    for m in dados:
        st.write(f"🏆 {m[1]}")
        st.write(m[2])
        st.write(f"Recompensa: {m[3]} XP | {m[4]} Core")

        if username != MASTER_USER:
            if st.button("Concluir Meta", key=f"meta{m[0]}"):

                c.execute("""
                    UPDATE users
                    SET xp=xp+?, core=core+?
                    WHERE id=?
                """, (m[3], m[4], st.session_state.user_id))

                registrar(
                    st.session_state.user_id,
                    "meta",
                    f"Concluiu meta: {m[1]}"
                )

                conn.commit()
                atualizar_nivel(st.session_state.user_id)
                st.success("Meta concluída!")
                st.rerun()