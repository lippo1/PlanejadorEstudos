from tkinter import *
from tkinter import ttk, messagebox
import datetime
import ttkbootstrap as ttb

from stats import EstatisticasJanela
from controller import insert, update, delete, show
from export import Exportador
import time  


class EstudoApp:
    def __init__(self, master):
        self.master = master
        master.title("Estudo+")
        master.geometry("1043x453")
        master.configure(background="#e9edf5")
        master.resizable(True, True)
        self.exportador = Exportador()


        self.setup_frames()
        self.setup_widgets()
        self.show()

    def setup_frames(self):
        self.frame_esquerda_cima = Frame(self.master, width=310, height=50, bg="#4fa882")
        self.frame_esquerda_cima.grid(row=0, column=0)

        self.frame_esquerda_baixo = Frame(self.master, width=310, height=403, bg="#feffff")
        self.frame_esquerda_baixo.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)

        self.frame_direita_cima = Frame(self.master, width=733, height=50, bg="#4fa882")
        self.frame_direita_cima.grid(row=0, column=1)

        self.frame_direita_baixo = Frame(self.master, width=733, height=403, bg="#feffff")
        self.frame_direita_baixo.grid(row=1, column=1, rowspan=2, sticky='NSEW', padx=1, pady=0)

        # Pesos para expansão: Linha 1 (baixa) expande verticalmente; Coluna 1 (direita) expande horizontalmente
        self.master.grid_rowconfigure(0, weight=0)  # Topo não expande verticalmente
        self.master.grid_rowconfigure(1, weight=1)  # Baixo expande verticalmente
        self.master.grid_columnconfigure(0, weight=0)  # Esquerda não expande horizontalmente (fixa)
        self.master.grid_columnconfigure(1, weight=1)  # Direita expande horizontalmente

    def setup_widgets(self):
        Label(self.frame_esquerda_cima, text='Controlador de estudos', font='Ivy 13 bold', bg="#4fa882",
              fg="#feffff").place(x=10, y=20)

        # Entradas
        self.add_label_entry("Matéria *", 10, 40, "materia")
        self.add_label_entry("Assunto *", 70, 100, "assunto")
        self.add_label_entry("Minutos *", 130, 160, "minutos", width=12)
        Label(self.frame_esquerda_baixo, text="Data *", bg="#feffff", fg="#403d3d", font="Ivy 10 bold").place(x=160, y=130)

        initial_date = datetime.date(2024, 1, 1)  # Or use datetime.date.today().replace(year=2024)
        self.entry_data = ttb.DateEntry(self.frame_esquerda_baixo, width=12, startdate=initial_date, bootstyle='primary')  # Add bootstyle for theming
        self.entry_data.place(x=160, y=159)

        self.add_label_entry("Descrição *", 190, 220, "descricao")

        # Botões:
        # ----- Frame superior direito:
        self.bt_controle = ttb.Button(
            self.frame_direita_cima, 
            text="Controle",  
            bootstyle="success",
            width=8 
        )
        self.bt_controle.place(x=1, y=19)


        # ----- Frame inferior esquerdo:
        self.bt_inserir = ttb.Button(
            self.frame_esquerda_baixo, 
            text="Inserir", 
            command=self.insert_ui, 
            bootstyle="success",
            width=8 
        )
        self.bt_inserir.place(x=15, y=280)

        self.bt_atualizar = ttb.Button(
            self.frame_esquerda_baixo, 
            text="Atualizar", 
            command=self.update_ui, 
            bootstyle="success",
            width=8
        )
        self.bt_atualizar.place(x=105, y=280)

        self.bt_delete = ttb.Button(
            self.frame_esquerda_baixo, 
            text="Deletar", 
            command=self.delete_ui, 
            bootstyle="success",
            width=8
        )
        self.bt_delete.place(x=195, y=280)

        self.bt_exportar = ttb.Button(
            self.frame_esquerda_baixo, 
            text="Exportar", 
            command=self.exportar_dados, 
            bootstyle="success",
            width=8 
        ) 
        self.bt_exportar.place(x=60, y=320)

        self.bt_stats = ttb.Button(
            self.frame_esquerda_baixo, 
            text="Info+", 
            command=self.abrir_estatisticas, 
            bootstyle="success",
            width=8
        ) 
        self.bt_stats.place(x=150, y=320)
        

        self.btn_timer = Button(self.frame_esquerda_baixo, text="Iniciar Timer", command=self.toggle_timer)
        self.btn_timer.place(x=15, y=350)

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
        for widget in self.frame_direita_baixo.winfo_children():
            widget.destroy()
        self.tree = show(self.frame_direita_baixo)



    def toggle_timer(self):
        if not self.timer_running:
            self.start_time = time.time()
            self.btn_timer.config(text="Parar Timer")
            self.timer_running = True
        else:
            elapsed = int((time.time() - self.start_time) / 60)  # Calcula minutos
            self.entry_minutos.delete(0, END)
            self.entry_minutos.insert(0, str(elapsed))
            self.btn_timer.config(text="Iniciar Timer")
            self.timer_running = False

    