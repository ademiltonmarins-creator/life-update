import streamlit as st
from database import c, conn
from utils import atualizar_nivel, registrar
from config import MASTER_USER

def loja():
    st.subheader("Loja")

    username = c.execute(
        "SELECT username FROM users WHERE id=?",
        (st.session_state.user_id,)
    ).fetchone()[0]

    # ===== ADMIN CADASTRA ITEM =====
    if username == MASTER_USER:
        st.subheader("Cadastrar Item")

        nome = st.text_input("Nome do item")
        desc = st.text_input("Descrição")
        preco = st.number_input("Preço",1,1000,10)
        tipo = st.selectbox("Tipo",["xp"])

        if st.button("Cadastrar"):
            c.execute("""
                INSERT INTO loja
                (nome,descricao,preco,tipo)
                VALUES (?,?,?,?)
            """,(nome,desc,preco,tipo))
            conn.commit()
            st.success("Item criado!")
            st.rerun()

        st.divider()

    saldo = c.execute(
        "SELECT core FROM users WHERE id=?",
        (st.session_state.user_id,)
    ).fetchone()[0]

    itens = c.execute(
        "SELECT id,nome,preco FROM loja"
    ).fetchall()

    for item in itens:
        st.write(f"{item[1]} — 💎 {item[2]}")

        if saldo >= item[2]:
            if st.button("Comprar", key=item[0]):
                c.execute("""
                    UPDATE users
                    SET core=core-?
                    WHERE id=?
                """,(item[2],st.session_state.user_id))

                conn.commit()
                st.success("Compra realizada!")
                st.rerun()
        else:
            st.button("Core insuficiente",
                      disabled=True,
                      key=f"lock{item[0]}")