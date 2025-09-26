import sqlite3 as lite
import os

def pegar_caminho_do_banco_de_dados():
    # Retorna o caminho para um arquivo banco.db na pasta home do usuário
    return os.path.join(os.path.expanduser("~"), "banco.db")


def criar_banco_de_dados_se_não_existir():
    caminho_bd = pegar_caminho_do_banco_de_dados()
    conexão = lite.connect(caminho_bd)
    with conexão:
        cursor = conexão.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS anotacoes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                materia     TEXT NOT NULL,
                assunto     TEXT NOT NULL,
                minutos     INTEGER NOT NULL CHECK(minutos > 0),
                data        TEXT NOT NULL,
                descricao   TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semana (
                domingo     TEXT,
                segunda     TEXT,
                terça       TEXT,
                quarta      TEXT,
                quinta      TEXT,
                sexta       TEXT,
                sábado      TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                data        TEXT NOT NULL,
                materia     TEXT NOT NULL,
                resumo      TEXT NOT NULL
            )       
                    
        """)
    conexão.close()

criar_banco_de_dados_se_não_existir()  

'''
    Comandos CRUD da tabela ANOTAÇÕES:
'''
def inserir_item_anotações(i):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "INSERT INTO anotacoes(materia, assunto, minutos, data, descricao) VALUES(?, ?, ?, ?, ?)"
            cursor.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao inserir: {e}")


# atualizar
def atualizar_item_anotações(i):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "UPDATE anotacoes SET materia = ?, assunto = ?, minutos = ?, data = ?, descricao = ? WHERE id = ?"
            cursor.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao atualizar: {e}")

# Delete
def deletar_item_anotações(i):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "DELETE FROM anotacoes WHERE id = ?"
            cursor.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao deletar: {e}")

'''
    Comandos da tabela SEMANA:
'''
def inserir_item_semana(coluna, valor):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conn = lite.connect(caminho_bd)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM semana")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO semana (domingo, segunda, terça, quarta, quinta, sexta, sábado) VALUES (?, ?, ?, ?, ?, ?, ?)", ('', '', '', '', '', '', ''))
            cursor.execute(f"SELECT {coluna} FROM semana")
            current = cursor.fetchone()[0] or ''
            new_val = current + (", " if current else "") + valor
            query = f"UPDATE semana SET {coluna} = ?"
            cursor.execute(query, (new_val,))
    except lite.Error as e:
        raise ValueError(f"Erro ao atualizar semana: {e}")

def deletar_item_semana(coluna, index):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conn = lite.connect(caminho_bd)
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {coluna} FROM semana")
            current = cursor.fetchone()[0] or ''
            subjects = [s.strip() for s in current.split(', ') if s.strip()]
            if index < 0 or index >= len(subjects):
                raise ValueError("Índice fora do intervalo.")
            del subjects[index]
            new_val = ', '.join(subjects)
            query = f"UPDATE semana SET {coluna} = ?"
            cursor.execute(query, (new_val,))
    except lite.Error as e:
        raise ValueError(f"Erro ao deletar item da semana: {e}")
    except ValueError as ve:
        raise ve

'''
    Comandos da tabela RESUMO:
'''  

def inserir_item_resumo(info):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "INSERT INTO resumos (data, materia, resumo) VALUES (?, ?, ?)"
            cursor.execute(query, info)
    except lite.Error as e:
        raise ValueError(f"Erro ao inserir resumo: {e}")

def atualizar_resumo_info(i):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "UPDATE resumos SET data = ?, materia = ?, resumo = ? WHERE id = ?"
            cursor.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao atualizar resumo: {e}")

def deletar_resumo_info(i):
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = "DELETE FROM resumos WHERE id = ?"
            cursor.execute(query, i)
    except lite.Error as e:
        raise ValueError(f"Erro ao deletar resumo: {e}")

'''
    No controller.py, a função que mostrará para a UI a partir da TreeView terá o nome 'mostrar' seguida da tabela.
'''
def tabela(nome):
    lista = []
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        conexão = lite.connect(caminho_bd)
        with conexão:
            cursor = conexão.cursor()
            query = f"SELECT * FROM {nome}"
            cursor.execute(query)
            info = cursor.fetchall()
            for i in info:
                lista.append(i)
    except lite.Error as e:
        raise ValueError(f"Erro ao mostrar {nome}: {e}")
    return lista
    
def tabela_anotações():
    return tabela("anotacoes")
    
def tabela_semana():
    return tabela("semana")

def tabela_resumos():
    return tabela("resumos")


def pegar_dados_semana():
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        con = lite.connect(caminho_bd)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM semana"
            cur.execute(query)
            return cur.fetchall() 
    except lite.Error as e:
        raise ValueError(f"Erro ao obter dados da semana: {e}")

def pegar_dados_resumo():
    lista = []
    try:
        caminho_bd = pegar_caminho_do_banco_de_dados()
        con = lite.connect(caminho_bd)
        with con:
            cur = con.cursor()
            query = "SELECT * FROM resumos"
            cur.execute(query)
            info = cur.fetchall()
            for i in info:
                lista.append(i)
    except lite.Error as e:
        raise ValueError(f"Erro ao obter dados dos resumos: {e}")
    return lista