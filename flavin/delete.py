import sqlite3


def deletar_filme(filme_id):
    connection = sqlite3.connect("filmes.db")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM filmes WHERE id = ?", (filme_id,))

    connection.commit()

    cursor.close()
    connection.close()
