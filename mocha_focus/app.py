import streamlit as st
import base64

from database import init_db
from views.login import login
from views.dashboard import dashboard
from views.tarefas import tarefas
from views.loja import loja
from views.metas import metas
from views.ranking import ranking
from views.historico import historico
from config import APP_TITLE

# ================= CONFIGURAÇÃO DA PÁGINA =================
st.set_page_config(
    page_title=APP_TITLE,
    layout="centered",  # melhor para smartphone
   initial_sidebar_state="collapsed"
)

# ================= FUNDO PERSONALIZADO =================
def aplicar_fundo():
    try:
        with open("mocha_focus/assets/background.png", "rb") as f:
            data = base64.b64encode(f.read()).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            background: rgba(0,0,0,0.75);
            padding: 2rem;
            border-radius: 15px;
            color: white;
        }}

        h1, h2, h3, h4, h5, h6, p, label {{
            color: white !important;
        }}

        .stButton>button {{
            border-radius: 10px;
            background-color: #4CAF50;
            color: white;
        }}

        .stProgress > div > div > div {{
            background-color: #00ffcc;
        }}
        </style>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.warning("Imagem de fundo não encontrada em assets/background.png")


# ================= INICIALIZAÇÃO =================
init_db()
aplicar_fundo()

# ================= CONTROLE DE SESSÃO =================
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ================= APP =================
if st.session_state.user_id:

    st.sidebar.title("🎮 Menu")

    menu = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Tarefas",
            "Metas",
            "Loja",
            "Ranking",
            "Histórico"
        ]
    )

    if menu == "Dashboard":
        dashboard()

    elif menu == "Tarefas":
        tarefas()

    elif menu == "Metas":
        metas()

    elif menu == "Loja":
        loja()

    elif menu == "Ranking":
        ranking()

    elif menu == "Histórico":
        historico()

    st.sidebar.divider()

    if st.sidebar.button("🚪 Sair"):
        st.session_state.user_id = None
        st.rerun()

else:

    login()




