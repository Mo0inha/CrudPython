import sqlite3


def criar_filme(titulo, diretor, ano):
    connection = sqlite3.connect("filmes.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS filmes (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, diretor TEXT, ano TEXT, imagem TEXT)"
    )

    cursor.execute("INSERT INTO filmes (titulo, diretor, ano) VALUES (?, ?, ?)", (titulo, diretor, ano))

    connection.commit()

    cursor.close()
    connection.close()
