import sqlite3 as lite

def create_db_if_not_exists():
    con = lite.connect('banco.db')
    with con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS anotacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia TEXT NOT NULL,
                assunto TEXT NOT NULL,
                minutos INTEGER NOT NULL CHECK(minutos > 0),
                data TEXT NOT NULL,
                descricao TEXT NOT NULL
            )
        """)
    con.close()

create_db_if_not_exists()  

# Insert
def insert_info(info):
    try:
        con = lite.connect('banco.db')
        with con:
            cur = con.cursor()
            query = "INSERT INTO anotacoes(materia, assunto, minutos, data, descricao) VALUES(?, ?, ?, ?, ?)"
            cur.execute(query, info)
    except lite.Error as e:
        raise ValueError(f"Erro ao inserir: {e}")

# Show
def show_info():
    lista = []
    try:
        con = lite.connect('banco.db')
        with con:
            cur = con.cursor()
            query = "SELECT * FROM anotacoes"
            cur.execute(query)
            info = cur.fetchall()
            for i in info:
                lista.append(i)
    except lite.Error as e:
        raise ValueError(f"Erro ao mostrar: {e}")
    return lista

# Update
def update_info(i):
    try:
        con = lite.connect('banco.db')
        with con:
            cur = con.cursor()
            query = "UPDATE anotacoes SET materia = ?, assunto = ?, minutos = ?, data = ?, descricao = ? WHERE id = ?"
            cur.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao atualizar: {e}")

# Delete
def delete_info(i):
    try:
        con = lite.connect('banco.db')
        with con:
            cur = con.cursor()
            query = "DELETE FROM anotacoes WHERE id = ?"
            cur.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao deletar: {e}")

# Nova função para totais por dia
def get_totals_by_date():
    totals = {}
    try:
        con = lite.connect('banco.db')
        with con:
            cur = con.cursor()
            query = "SELECT data, SUM(minutos) FROM anotacoes GROUP BY data"
            cur.execute(query)
            for row in cur.fetchall():
                totals[row[0]] = row[1]
    except lite.Error as e:
        raise ValueError(f"Erro ao calcular totais: {e}")
    return totals