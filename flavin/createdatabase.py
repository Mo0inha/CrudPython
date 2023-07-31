import sqlite3

def criar_tabela_filmes():
    conn = sqlite3.connect("filmes.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filmes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            diretor TEXT NOT NULL,
            ano INTEGER NOT NULL
        )
    """)

    conn.commit()

    cursor.close()
    conn.close()


criar_tabela_filmes()
