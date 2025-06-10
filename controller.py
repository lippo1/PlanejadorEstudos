from tkinter import messagebox
from view import insert_info, update_info, delete_info, show_info
from tkinter.ttk import Treeview, Scrollbar

def insert(dados, callback):
    if dados[0] == '':
        messagebox.showerror("Erro", "Campo 'matéria' não pode ser vazio.")
    else:
        insert_info(dados)
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso.")
        callback()

def update(tree, get_dados, callback):
    try:
        item = tree.focus()
        valores = tree.item(item)['values']
        id_ = valores[0]
        novos_dados = get_dados()
        update_info(novos_dados + [id_])
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso.")
        callback()
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha na tabela.")

def delete(tree, callback):
    try:
        item = tree.focus()
        id_ = [tree.item(item)['values'][0]]
        delete_info(id_)
        messagebox.showinfo("Sucesso", "Dados deletados com sucesso.")
        callback()
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha.")

def show(frame):
    dados = show_info()
    colunas = ['ID', 'Matéria', 'Assunto', 'Minutos', 'Data', 'Descrição']
    tree = Treeview(frame, columns=colunas, show='headings')
    for i, col in enumerate(colunas):
        tree.heading(col, text=col)
        tree.column(col, anchor='center')
    for linha in dados:
        tree.insert('', 'end', values=linha)
    tree.grid(row=0, column=0, sticky='nsew')
    Scrollbar(frame, orient='vertical', command=tree.yview).grid(row=0, column=1, sticky='ns')
    return tree
