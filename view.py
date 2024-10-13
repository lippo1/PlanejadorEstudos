import sqlite3 as lite

con = lite.connect('banco.db')


# Insert
def insert_info(info):
    with con:
        cur = con.cursor()
        query = "INSERT INTO anotacoes(materia, assunto, minutos, data, descricao) VALUES(?, ?, ?, ?, ?)"
        cur.execute(query, info)


# Update
def show_info():
    lista = []
    with con:
        cur = con.cursor()
        query = "SELECT * FROM anotacoes"
        cur.execute(query)
        info = cur.fetchall()

        for i in info:
            lista.append(i)
    return lista


# Read
def update_info(i):
    with con:
        cur = con.cursor()
        query = "UPDATE anotacoes SET materia = ?, assunto = ?, minutos = ?, data = ?, descricao = ? WHERE id = ?"
        cur.execute(query, i)


# Delete
def delete_info(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM anotacoes WHERE id = ?"
        cur.execute(query, i)

