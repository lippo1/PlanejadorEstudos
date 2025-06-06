import sqlite3 as lite

con = lite.connect('banco.db')

with con:
    cur = con.cursor()
    cur.execute("CREATE TABLE anotacoes"
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "materia TEXT, "
                "assunto TEXT, "
                "minutos INTEGER, "
                "data text, "
                "descricao TEXT)")