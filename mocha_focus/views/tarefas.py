import streamlit as st
from datetime import datetime
from database import c, conn
from utils import atualizar_nivel, registrar
from config import MASTER_USER

def tarefas():
    st.subheader("Tarefas")

    username = c.execute(
        "SELECT username FROM users WHERE id=?",
        (st.session_state.user_id,)
    ).fetchone()[0]

    # ===== Apenas admin pode criar tarefas =====
    if username == MASTER_USER:
        st.subheader("Criar Nova Tarefa")

        titulo = st.text_input("Título da Tarefa")
        tipo = st.selectbox("Tipo", ["geral", "estudo", "treino", "rotina"])
        xp = st.number_input("XP Recompensa", 1, 100, 10)
        core = st.number_input("Core Recompensa", 1, 50, 5)

        if st.button("Adicionar Tarefa"):
            if not titulo.strip():
                st.error("Digite um título para a tarefa.")
            else:
                c.execute("""
                    INSERT INTO tarefas
                    (user_id, titulo, tipo, xp, core, data_criacao)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    st.session_state.user_id,
                    titulo,
                    tipo,
                    xp,
                    core,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                st.success("Tarefa criada com sucesso!")
                st.rerun()

    st.divider()

    # ===== Usuários concluem tarefas =====
    tarefas_pendentes = c.execute("""
        SELECT id, user_id, titulo, tipo, xp, core
        FROM tarefas
        WHERE status='pendente'
        ORDER BY data_criacao ASC
    """).fetchall()

    if not tarefas_pendentes:
        st.info("Nenhuma tarefa pendente.")
        return

    for t in tarefas_pendentes:
        st.write(f"📌 {t[2]} ({t[3]}) — XP:{t[4]} | Core:{t[5]}")

        # Só o usuário dono pode concluir
        if username != MASTER_USER and st.button("Concluir", key=t[0]):
            c.execute("""
                UPDATE tarefas
                SET status='concluida', data_conclusao=?
                WHERE id=?
            """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), t[0]))

            c.execute("""
                UPDATE users
                SET xp = xp + ?, core = core + ?
                WHERE id = ?
            """, (t[4], t[5], st.session_state.user_id))

            conn.commit()
            atualizar_nivel(st.session_state.user_id)
            registrar(st.session_state.user_id, "tarefa", f"Concluiu {t[2]}")
            st.success("Tarefa concluída!")
            st.rerun()