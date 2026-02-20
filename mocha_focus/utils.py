import os
from datetime import datetime
from database import c, conn
from config import BASE_DIR

def calcular_nivel(xp):
    return (xp // 100) + 1

def caminho_avatar(classe, nivel):
    if nivel >= 10:
        lvl = "lvl3"
    elif nivel >= 5:
        lvl = "lvl2"
    else:
        lvl = "lvl1"

    caminho_rel = f"assets/avatars/{classe}_{lvl}.png"
    return os.path.join(BASE_DIR, caminho_rel)

def atualizar_avatar_por_nivel(user_id):
    classe, nivel = c.execute(
        "SELECT classe, nivel FROM users WHERE id=?",
        (user_id,)
    ).fetchone()

    caminho = caminho_avatar(classe, nivel)

    if os.path.exists(caminho):
        c.execute("UPDATE users SET avatar=? WHERE id=?",
                  (caminho, user_id))
        conn.commit()

def atualizar_nivel(user_id):
    xp = c.execute("SELECT xp FROM users WHERE id=?",
                   (user_id,)).fetchone()[0]
    nivel = calcular_nivel(xp)

    c.execute("UPDATE users SET nivel=? WHERE id=?",
              (nivel, user_id))
    conn.commit()

    atualizar_avatar_por_nivel(user_id)

def registrar(user_id, tipo, desc):
    c.execute("""INSERT INTO historico
        (user_id,tipo,descricao,data)
        VALUES (?,?,?,?)""",
        (user_id, tipo, desc,
         datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()