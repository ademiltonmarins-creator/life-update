import streamlit as st
import os
from database import c

def dashboard():
    user = c.execute("""SELECT username,xp,nivel,
                        core,avatar,classe
                        FROM users WHERE id=?""",
                        (st.session_state.user_id,)
                        ).fetchone()

    st.title(f"{user[0]} — Nível {user[2]}")

    if user[4] and os.path.exists(user[4]):
        st.image(user[4], width=150)

    progresso = user[1] % 100
    st.progress(progresso)
    st.write(f"XP: {user[1]}")
    st.write(f"💎 Core: {user[3]}")
    st.write(f"Classe: {user[5]}")