from tkinter import messagebox
from tkinter.ttk import Treeview
import ttkbootstrap as ttb


from database import inserir_item_anotações, atualizar_item_anotações, deletar_item_anotações
from database import tabela_anotações, tabela_semana, tabela_resumos
from database import inserir_item_semana, deletar_item_semana
from database import  inserir_item_resumo, atualizar_resumo_info, deletar_resumo_info

'''
    Pega os dados do BD e mostra na Interface Tkinter.
'''

def inserir_anotações_treeview(dados, callback):
    if dados[0] == '':
        messagebox.showerror("Erro", "Campo 'matéria' não pode ser vazio.")
    else:
        inserir_item_anotações(dados)
        messagebox.showinfo("Sucesso", "Dados inseridos com sucesso.")
        callback()


def atualizar_anotações_treeview(tree, pegar_dados_interface_anotações, callback):
    try:
        item = tree.focus()
        valores = tree.item(item)['values']
        id_ = valores[0]
        novos_dados = pegar_dados_interface_anotações()
        atualizar_item_anotações(novos_dados + [id_])
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso.")
        callback()
        
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha na tabela.")


def deletar_anotações_treeview(tree, callback):
    try:
        item = tree.focus()
        id_ = [tree.item(item)['values'][0]]
        deletar_item_anotações(id_)
        messagebox.showinfo("Sucesso", "Dados deletados com sucesso.")
        callback()
        
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha.")


def atualizar_semana_treeview(coluna, valor, callback):
    inserir_item_semana(coluna, valor)
    messagebox.showinfo("Sucesso", "Horário atualizado com sucesso.")
    callback()


def deletar_semana_treeview(coluna, index, callback):
    try:
        deletar_item_semana(coluna, index)
        messagebox.showinfo("Sucesso", "Item deletado com sucesso.")
    except ValueError as e:
        messagebox.showerror("Erro", str(e))
        return
    callback()
    

def inserir_resumo_treeview(dados, callback):
    if '' in dados:
        messagebox.showerror("Erro", "Preencha todos os campos.")
    else:
        inserir_item_resumo(dados)
        messagebox.showinfo("Sucesso", "Resumo inserido com sucesso.")
        callback()


def atualizar_resumo_treeview(tree, pegar_dados_interface_anotações, callback):
    try:
        item = tree.focus()
        valores = tree.item(item)['values']
        id_ = valores[0]
        novos_dados = pegar_dados_interface_anotações()
        atualizar_resumo_info(novos_dados + [id_])
        messagebox.showinfo("Sucesso", "Resumo atualizado com sucesso.")
        callback()
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha na tabela.")


def deletar_resumo_treeview(tree, callback):
    try:
        item = tree.focus()
        id_ = [tree.item(item)['values'][0]]
        deletar_resumo_info(id_)
        messagebox.showinfo("Sucesso", "Resumo deletado com sucesso.")
        callback()
    except IndexError:
        messagebox.showerror("Erro", "Selecione uma linha.")
 
        
def mostrar_tabela_anotações(frame):
    dados = tabela_anotações()
    colunas = ['ID', 'Matéria', 'Assunto', 'Minutos', 'Data', 'Descrição']
    tree = Treeview(frame, columns=colunas, show='headings')
    for i, col in enumerate(colunas):
        tree.heading(col, text=col if col != 'ID' else '')
        if col == 'ID':
            tree.column(col, width=0, minwidth=0, stretch=False)
        else:
            tree.column(col, anchor='center', minwidth=100, width=100)
    for linha in dados:
        tree.insert('', 'end', values=linha)
    tree.grid(row=0, column=0, sticky='nsew')


    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    v_scroll = ttb.Scrollbar(frame, orient='vertical', command=tree.yview, bootstyle='round')
    v_scroll.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=v_scroll.set)

   
    h_scroll = ttb.Scrollbar(frame, orient='horizontal', command=tree.xview, bootstyle='round')
    h_scroll.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=h_scroll.set)
    return tree


def mostrar_tabela_semana(frame):
    dados = tabela_semana()
    colunas = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']
    tree = Treeview(frame, columns=colunas, show='headings')
    for i, col in enumerate(colunas):
        tree.heading(col, text=col)
        tree.column(col, anchor='center', minwidth=100, width=100)

    if dados: 
        day_lists = []
        for i in range(7):
            column_value = dados[0][i] or ''
            subjects = [s.strip() for s in column_value.split(', ') if s.strip()]
            day_lists.append(subjects)
        
        max_len = max(len(lst) for lst in day_lists) if day_lists else 0
        
        for row_idx in range(max_len):
            row = [day_lists[col_idx][row_idx] if row_idx < len(day_lists[col_idx]) else '' for col_idx in range(7)]
            tree.insert('', 'end', values=row)
    
    tree.grid(row=0, column=0, sticky='nsew')


    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    v_scroll = ttb.Scrollbar(frame, orient='vertical', command=tree.yview, bootstyle='round')
    v_scroll.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=v_scroll.set)

    h_scroll = ttb.Scrollbar(frame, orient='horizontal', command=tree.xview, bootstyle='round')
    h_scroll.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=h_scroll.set)
    return tree


def mostrar_tabela_resumos(frame):
    dados = tabela_resumos()
    colunas = ['ID', 'Data', 'Matéria', 'Resumo']
    tree = Treeview(frame, columns=colunas, show='headings')
    for i, col in enumerate(colunas):
        tree.heading(col, text=col if col != 'ID' else '')
        if col == 'ID':
            tree.column(col, width=0, minwidth=0, stretch=False)
        elif col == 'Resumo':
            tree.column(col, anchor='w', minwidth=200, width=400)
        else:
            tree.column(col, anchor='center', minwidth=100, width=100)
    for linha in dados:
        linha = list(linha)
        linha[3] = linha[3].replace('\n', ' ')
        tree.insert('', 'end', values=linha)
    tree.grid(row=0, column=0, sticky='nsew')

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    v_scroll = ttb.Scrollbar(frame, orient='vertical', command=tree.yview, bootstyle='round')
    v_scroll.grid(row=0, column=1, sticky='ns')
    tree.configure(yscrollcommand=v_scroll.set)

    h_scroll = ttb.Scrollbar(frame, orient='horizontal', command=tree.xview, bootstyle='round')
    h_scroll.grid(row=1, column=0, sticky='ew')
    tree.configure(xscrollcommand=h_scroll.set)
    return tree