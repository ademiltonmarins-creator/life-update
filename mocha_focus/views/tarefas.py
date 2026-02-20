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

    # ================= CRIAR TAREFA (ADMIN) =================
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
                    (user_id, titulo, tipo, xp, core, data_criacao, status)
                    VALUES (?, ?, ?, ?, ?, ?, 'pendente')
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

    # ================= LISTAR TAREFAS =================
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
        st.markdown(f"### 📌 {t[2]}")
        st.write(f"Tipo: {t[3]} | XP: {t[4]} | Core: {t[5]}")

        col1, col2, col3 = st.columns(3)

        # ===== CONCLUIR (usuário comum) =====
        if username != MASTER_USER:
            if col1.button("Concluir", key=f"concluir_{t[0]}"):
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

        # ===== EDITAR / EXCLUIR (ADMIN) =====
        if username == MASTER_USER:

            if col2.button("Editar", key=f"editar_{t[0]}"):
                st.session_state["editar_tarefa"] = t[0]

            if col3.button("Excluir", key=f"excluir_{t[0]}"):
                c.execute("DELETE FROM tarefas WHERE id=?", (t[0],))
                conn.commit()
                st.success("Tarefa excluída!")
                st.rerun()

        st.divider()

    # ================= ÁREA DE EDIÇÃO =================
    if "editar_tarefa" in st.session_state:
        tarefa_id = st.session_state["editar_tarefa"]

        tarefa = c.execute("""
            SELECT titulo, tipo, xp, core
            FROM tarefas
            WHERE id=?
        """, (tarefa_id,)).fetchone()

        if tarefa:
            st.subheader("Editar Tarefa")

            novo_titulo = st.text_input("Título", tarefa[0])
            tipos = ["geral", "estudo", "treino", "rotina"]
            novo_tipo = st.selectbox("Tipo", tipos, index=tipos.index(tarefa[1]))
            novo_xp = st.number_input("XP", 1, 100, tarefa[2])
            novo_core = st.number_input("Core", 1, 50, tarefa[3])

            if st.button("Salvar Alterações"):
                c.execute("""
                    UPDATE tarefas
                    SET titulo=?, tipo=?, xp=?, core=?
                    WHERE id=?
                """, (novo_titulo, novo_tipo, novo_xp, novo_core, tarefa_id))

                conn.commit()
                del st.session_state["editar_tarefa"]
                st.success("Tarefa atualizada!")
                st.rerun()
