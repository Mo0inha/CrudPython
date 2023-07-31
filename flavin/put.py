import sqlite3


def salvar_modificacoes(filme_id, titulo, diretor, ano):
    connection = sqlite3.connect("filmes.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE filmes SET titulo = ?, diretor = ?, ano = ? WHERE id = ?", (titulo, diretor, ano, filme_id))

    connection.commit()

    cursor.close()
    connection.close()
