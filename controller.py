from tkinter import messagebox
from view import insert_info, update_info, delete_info, show_info
from tkinter.ttk import Treeview, Scrollbar
import ttkbootstrap as ttb

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
        tree.column(col, anchor='center', minwidth=100, width=100)
    for linha in dados:
        tree.insert('', 'end', values=linha)
    tree.grid(row=0, column=0, sticky='nsew')

    # Configurações para expansão
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Barra de scroll vertical
    v_scroll = ttb.Scrollbar(frame, orient='vertical', command=tree.yview, bootstyle='round')  # Estilo arredondado
    v_scroll.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=v_scroll.set)

    # Barra de scroll horizontal
    h_scroll = ttb.Scrollbar(frame, orient='horizontal', command=tree.xview, bootstyle='round')  # Estilo arredondado
    h_scroll.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=h_scroll.set)
    return tree
