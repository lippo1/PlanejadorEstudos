from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from stats import EstatisticasJanela
from controller import insert, update, delete, show
from export import Exportador


class EstudoApp:
    def __init__(self, master):
        self.master = master
        master.title("Controlador de Estudos")
        master.geometry("1043x453")
        master.configure(background="#e9edf5")
        self.exportador = Exportador()


        self.setup_frames()
        self.setup_widgets()
        self.show()

    def setup_frames(self):
        self.frame_esquerda_cima = Frame(self.master, width=310, height=50, bg="#4fa882")
        self.frame_esquerda_cima.grid(row=0, column=0)

        self.frame_esquerda_baixo = Frame(self.master, width=310, height=403, bg="#feffff")
        self.frame_esquerda_baixo.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)

        self.frame_direita = Frame(self.master, width=588, height=403, bg="#feffff")
        self.frame_direita.grid(row=0, column=1, rowspan=2, sticky='NSEW', padx=1, pady=0)

    def setup_widgets(self):
        Label(self.frame_esquerda_cima, text='Controlador de estudos', font='Ivy 13 bold', bg="#4fa882",
              fg="#feffff").place(x=10, y=20)

        # Entradas
        self.add_label_entry("Matéria *", 10, 40, "materia")
        self.add_label_entry("Assunto *", 70, 100, "assunto")
        self.add_label_entry("Minutos estudados *", 130, 160, "minutos", width=12)
        Label(self.frame_esquerda_baixo, text="Data (mm/dd/yy)*", bg="#feffff", fg="#403d3d", font="Ivy 10 bold").place(x=160, y=130)
        self.entry_data = DateEntry(self.frame_esquerda_baixo, width=12, year=2024)
        self.entry_data.place(x=160, y=160)
        self.add_label_entry("Descrição *", 190, 220, "descricao")

        # Botões
        Button(self.frame_esquerda_baixo, text="Inserir",      command=self.insert_ui, bg="#038cfc", fg="white").place(x=15, y=280)
        Button(self.frame_esquerda_baixo, text="Atualizar",    command=self.update_ui, bg="#263238", fg="white").place(x=105, y=280)
        Button(self.frame_esquerda_baixo, text="Deletar",      command=self.delete_ui, bg="#ef5350", fg="white").place(x=195, y=280)
        Button(self.frame_esquerda_baixo, text="Exportar",     command=self.exportar_dados).place(x=60, y=320)
        Button(self.frame_esquerda_baixo, text="Estatísticas", command=self.abrir_estatisticas).place(x=150, y=320)

    def add_label_entry(self, text, y_label, y_entry, attr, width=45):
        Label(self.frame_esquerda_baixo, text=text, font="Ivy 10 bold", bg="#feffff", fg="#403d3d").place(x=10, y=y_label)
        setattr(self, f"entry_{attr}", Entry(self.frame_esquerda_baixo, width=width))
        getattr(self, f"entry_{attr}").place(x=15, y=y_entry)

    def insert_ui(self):
        dados = self.get_dados()
        insert(dados, self.show)

    def update_ui(self):
        update(self.tree, self.get_dados, self.show)

    def delete_ui(self):
        delete(self.tree, self.show)

    def exportar_dados(self):
        self.exportador.exportar_excel()


    def abrir_estatisticas(self):
        estat_win = Toplevel()
        EstatisticasJanela(estat_win)

    def get_dados(self):
        return [
            self.entry_materia.get(),
            self.entry_assunto.get(),
            self.entry_minutos.get(),
            self.entry_data.get(),
            self.entry_descricao.get()
        ]

    def show(self):
        for widget in self.frame_direita.winfo_children():
            widget.destroy()
        self.tree = show(self.frame_direita)
