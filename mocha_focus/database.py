import sqlite3
from config import DB_NAME

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
c = conn.cursor()

def init_db():
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        classe TEXT DEFAULT 'guerreiro',
        avatar TEXT DEFAULT '',
        xp INTEGER DEFAULT 0,
        nivel INTEGER DEFAULT 1,
        core INTEGER DEFAULT 0
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS tarefas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        titulo TEXT,
        tipo TEXT,
        xp INTEGER,
        core INTEGER,
        status TEXT DEFAULT 'pendente',
        data_criacao TEXT,
        data_conclusao TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS loja(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        preco INTEGER,
        tipo TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS historico(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        tipo TEXT,
        descricao TEXT,
        data TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS conquistas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        nome TEXT,
        data TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS metas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        xp INTEGER,
        core INTEGER,
        ativa INTEGER DEFAULT 1
    )""")

    conn.commit()