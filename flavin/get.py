import sqlite3


def exibir_filmes(busca=None):
    connection = sqlite3.connect("filmes.db")
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS filmes (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT, diretor TEXT, ano TEXT, imagem TEXT)"
    )

    if busca:
        cursor.execute(
            "SELECT * FROM filmes WHERE titulo LIKE ? OR diretor LIKE ? OR ano LIKE ?",
            (f"%{busca}%", f"%{busca}%", f"%{busca}%"),
        )
    else:
        cursor.execute("SELECT * FROM filmes")

    filmes = cursor.fetchall()

    cursor.close()
    connection.close()

    filmes_dict = []
    for filme in filmes:
        filme_dict = {
            "id": filme[0],
            "titulo": filme[1],
            "diretor": filme[2],
            "ano": filme[3],
            "imagem": filme[4]
        }
        filmes_dict.append(filme_dict)

    return filmes_dict


def selecionar_filme(filme_id):
    connection = sqlite3.connect("filmes.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,))

    filme = cursor.fetchone()

    cursor.close()
    connection.close()

    if filme:
        filme_dict = {
            "id": filme[0],
            "titulo": filme[1],
            "diretor": filme[2],
            "ano": filme[3],
            "imagem": filme[4]
        }
        return filme_dict
    else:
        return None
