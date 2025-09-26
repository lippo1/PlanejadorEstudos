from tkinter import *
from tkinter import ttk, messagebox
import ttkbootstrap as ttb
from datetime import date
 
from stats import EstatisticasJanela
from controller import inserir_anotações_treeview, atualizar_anotações_treeview, deletar_anotações_treeview, mostrar_tabela_anotações, mostrar_tabela_semana, mostrar_tabela_resumos
from controller import atualizar_semana_treeview, deletar_semana_treeview
from controller import inserir_resumo_treeview, atualizar_resumo_treeview, deletar_resumo_treeview
from export import Exportador


class EstudoApp:
    def __init__(self, master):
        self.master = master
        master.title("Controlador de estudos")
        master.geometry("1043x453")
        master.configure(background="#e9edf5")
        master.resizable(True, True)
        self.exportador = Exportador()

        self.setup_frames()
        self.setup_widgets()
        self.exibir_tabela_anotações()


    def setup_frames(self):
        
        self.frame_esquerda_cima = Frame(self.master, width=310, height=50, bg="#4fa882")
        self.frame_esquerda_cima.grid(row=0, column=0)


        self.frame_esquerda_controle = Frame(self.master, width=310, height=403, bg="#feffff")
        self.frame_esquerda_controle.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)       
        self.frame_esquerda_semana = Frame(self.master, width=310, height=403, bg="#feffff")
        self.frame_esquerda_resumos = Frame(self.master, width=310, height=403, bg="#feffff")

        self.frame_direita_cima_botões = Frame(self.master, width=733, height=50, bg="#4fa882")
        self.frame_direita_cima_botões.grid(row=0, column=1)

        self.frame_direita_baixo_tabelas = Frame(self.master, width=733, height=403, bg="#feffff")
        self.frame_direita_baixo_tabelas.grid(row=1, column=1, rowspan=2, sticky='NSEW', padx=1, pady=0)

        # Pesos para expansão (igual ao original)
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)


    def add_label_entry(self, text, y_label, y_entry, attr, frame, width=45, x_label=10, x_entry=15):
        Label(frame, 
              text=text, 
              font="Ivy 10 bold", 
              bg="#feffff", 
              fg="#403d3d"
              ).place(x=x_label, y=y_label)
        setattr(self, f"entry_{attr}", Entry(frame, width=width))
        getattr(self, f"entry_{attr}").place(x=x_entry, y=y_entry)
                
    

    def adicionar_botão(self, text, command, bootstyle, x, y, frame, width=8, attr=None):
        button = ttb.Button(
            frame,  # Agora dinâmico
            text=text, 
            command=command, 
            bootstyle=bootstyle,
            width=width)
        button.place(x=x, y=y)
        if attr:
            setattr(self, f"bt_{attr}", button)
        
        
    def setup_widgets(self):
        
        '''
            Título:
        '''
        Label(self.frame_esquerda_cima, text='Controlador de estudos', font='Ivy 13 bold', bg="#4fa882",
            fg="#feffff").place(x=10, y=20)

        '''
            Botões de cima para controlar os frames:
        '''
        self.adicionar_botão("Controle", self.exibir_tabela_anotações, "primary", 1, 19, frame=self.frame_direita_cima_botões, attr="controle")
        self.adicionar_botão("Semana", self.exibir_tabela_semana, "primary", 91, 19, frame=self.frame_direita_cima_botões, attr="semana") 
        self.adicionar_botão("Resumos", self.exibir_tabela_resumos, "primary", 181, 19, frame=self.frame_direita_cima_botões, attr="resumos")
          

        '''
            Lado esquerdo do frame CONTROLE:
        '''
        self.add_label_entry("Matéria *", 10, 40, "materia", frame=self.frame_esquerda_controle)
        self.add_label_entry("Assunto *", 70, 100, "assunto", frame=self.frame_esquerda_controle)
        self.add_label_entry("Minutos *", 130, 160, "minutos", frame=self.frame_esquerda_controle, width=12)
        
        # -> Data:
        Label(self.frame_esquerda_controle, text="Data *", bg="#feffff", fg="#403d3d", font="Ivy 10 bold").place(x=160, y=130)
        self.entry_data = ttb.DateEntry(self.frame_esquerda_controle, width=12, startdate=None, dateformat='%Y-%m-%d', bootstyle='primary')
        self.entry_data.place(x=160, y=159)
        
        self.add_label_entry("Descrição *", 190, 220, "descricao", frame=self.frame_esquerda_controle)
        
        self.adicionar_botão("Inserir", self.inserir_anotações, "success", 15, 280, frame=self.frame_esquerda_controle, attr="inserir")
        self.adicionar_botão("Atualizar", self.atualizar_anotações, "warning", 105, 280, frame=self.frame_esquerda_controle, attr="atualizar")
        self.adicionar_botão("Deletar", self.deletar_anotações, "danger", 195, 280, frame=self.frame_esquerda_controle, attr="deletar")
        self.adicionar_botão("Exportar", self.exportador.exportar_anotacoes, "default", 60, 320, frame=self.frame_esquerda_controle, attr="exportar")
        self.adicionar_botão("Info+", self.abrir_estatisticas_anotações, "info", 150, 320, frame=self.frame_esquerda_controle, attr="stats")
        # Botão que está escondido:
        self.bt_confirmar_controle = ttk.Button(self.frame_esquerda_controle, text="Confirmar", command=self.confirmar_atualizações_controle, width=8)
        self.bt_confirmar_controle.place_forget()
        
        '''
            Lado esquerdo do frame SEMANA:
        '''
        self.add_label_entry("Matéria *", 10, 40, "materia_horarios", frame=self.frame_esquerda_semana)

        Label(self.frame_esquerda_semana, text="Dia da Semana *", font="Ivy 10 bold", bg="#feffff", fg="#403d3d").place(x=10, y=70)
        self.combo_dia = ttk.Combobox(self.frame_esquerda_semana, values=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'], state="readonly")
        self.combo_dia.place(x=15, y=100)

        self.adicionar_botão("Confirmar", self.confirmar_horario, "success", 15, 140, frame=self.frame_esquerda_semana, width=10, attr="confirmar_horario")
        
        self.add_label_entry("Linha *", 70, 100, "linha_horarios", frame=self.frame_esquerda_semana, width=10, x_entry=225, x_label=225)
        
        self.adicionar_botão("Deletar", self.deletar_horario, "danger", 219, 140, frame=self.frame_esquerda_semana, attr="deletar_horario")
        self.adicionar_botão("Exportar", self.exportador.exportar_semana, "default", 121, 140, frame=self.frame_esquerda_semana)
        
        '''
            Lado esquerdo do frame RESUMOS:
        '''
        
        self.add_label_entry("Matéria *", 10, 40, "materia_resumo", frame=self.frame_esquerda_resumos)
        
        
        Label(self.frame_esquerda_resumos, text="Data *", font="Ivy 10 bold", bg="#feffff", fg="#403d3d").place(x=10, y=70)
        self.entry_data_resumo = ttb.DateEntry(self.frame_esquerda_resumos, width=12, dateformat='%Y-%m-%d', bootstyle='primary')
        self.entry_data_resumo.place(x=15, y=95)

        

        Label(self.frame_esquerda_resumos, text="Resumo *", font="Ivy 10 bold", bg="#feffff", fg="#403d3d").place(x=10, y=130)
        self.text_resumo = Text(self.frame_esquerda_resumos, height=10, width=43, wrap='word')
        self.text_resumo.place(x=15, y=160)

        self.adicionar_botão("Inserir", self.inserir_resumo, "success", 15, 330, frame=self.frame_esquerda_resumos, attr="inserir_resumo_treeview")
        self.adicionar_botão("Atualizar", self.atualizar_resumo, "warning", 105, 330, frame=self.frame_esquerda_resumos, attr="atualizar_resumo")
        self.adicionar_botão("Deletar", self.deletar_resumo, "danger", 195, 330, frame=self.frame_esquerda_resumos, attr="deletar_resumo")
        self.adicionar_botão("Exportar", self.exportador.exportar_resumos, "default", 195, 95, frame=self.frame_esquerda_resumos, attr="exportar_resumo")
        # Botão que está escondido:
        self.bt_confirmar_resumo = ttb.Button(self.frame_esquerda_resumos, text="Confirmar", command=self.confirmar_atualizações_resumo, bootstyle="info", width=8)
        self.bt_confirmar_resumo.place_forget()

    '''
        Comandos da tabela ANOTAÇÕES / CONTROLE:
    '''
    def inserir_anotações(self):
        dados = self.pegar_dados_interface_anotações()
        inserir_anotações_treeview(dados, self.exibir_tabela_anotações)

    def atualizar_anotações(self):
        try:
            item = self.tree.focus()
            if not item:
                messagebox.showerror("Erro", "Selecione uma linha na tabela.")
                return
            valores = self.tree.item(item)['values']
     
            self.entry_materia.delete(0, END)
            self.entry_materia.insert(0, valores[1])  
            self.entry_assunto.delete(0, END)
            self.entry_assunto.insert(0, valores[2])  
            self.entry_minutos.delete(0, END)
            self.entry_minutos.insert(0, valores[3])  
            data_date = date.fromisoformat(valores[4])
            self.entry_data.set_date(data_date)
            self.entry_descricao.delete(0, END)
            self.entry_descricao.insert(0, valores[5])  
            
            
            self.bt_confirmar_controle.place(x=105, y=250) 
            
        except IndexError:
            messagebox.showerror("Erro", "Selecione uma linha na tabela.")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida na linha selecionada.")
            

    def confirmar_atualizações_controle(self):
        atualizar_anotações_treeview(self.tree, self.pegar_dados_interface_anotações, self.exibir_tabela_anotações)

        self.bt_confirmar_controle.place_forget()

        self.entry_materia.delete(0, END)
        self.entry_assunto.delete(0, END)
        self.entry_minutos.delete(0, END)
        self.entry_data.entry.delete(0, END)  
        self.entry_descricao.delete(0, END)
        
    
    def deletar_anotações(self):
        deletar_anotações_treeview(self.tree, self.exibir_tabela_anotações)

    def exportar_anotações(self):
        self.exportador.exportar_excel()

    def abrir_estatisticas_anotações(self):
        estat_win = Toplevel()
        EstatisticasJanela(estat_win)

    def pegar_dados_interface_anotações(self):
        return [
            self.entry_materia.get(),
            self.entry_assunto.get(),
            self.entry_minutos.get(),
            self.entry_data.entry.get(),
            self.entry_descricao.get()]
        
    '''
        Comandos da tabela SEMANA:
    '''
    def confirmar_horario(self):
        materia = self.entry_materia_horarios.get()
        dia = self.combo_dia.get()
        if not materia or not dia:
            messagebox.showerror("Erro", "Preencha matéria e dia.")
            return
        dias_map = {
            'Domingo': 'domingo',
            'Segunda': 'segunda',
            'Terça': 'terça',
            'Quarta': 'quarta',
            'Quinta': 'quinta',
            'Sexta': 'sexta',
            'Sábado': 'sábado'
        }
        coluna = dias_map[dia]
        atualizar_semana_treeview(coluna, materia, self.exibir_tabela_semana)
        
    def deletar_horario(self):
        dia = self.combo_dia.get()
        linha_str = self.entry_linha_horarios.get()
        if not dia or not linha_str:
            messagebox.showerror("Erro", "Preencha dia e linha.")
            return
        try:
            linha = int(linha_str) - 1 
            if linha < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Linha deve ser um número positivo.")
            return
        dias_map = {
            'Domingo': 'domingo',
            'Segunda': 'segunda',
            'Terça': 'terça',
            'Quarta': 'quarta',
            'Quinta': 'quinta',
            'Sexta': 'sexta',
            'Sábado': 'sábado'
        }
        coluna = dias_map[dia]
        deletar_semana_treeview(coluna, linha, self.exibir_tabela_semana)
    
    '''
        Comandos da tabela RESUMO:
    '''
    def inserir_resumo(self):
        dados = self.pegar_dados_resumo()
        inserir_resumo_treeview(dados, self.exibir_tabela_resumos)

    def atualizar_resumo(self):
        try:
            item = self.tree.focus()
            if not item:
                messagebox.showerror("Erro", "Selecione uma linha na tabela.")
                return
            valores = self.tree.item(item)['values']

            data_date = date.fromisoformat(valores[1])
            self.entry_data_resumo.set_date(data_date)
            self.entry_materia_resumo.delete(0, END)
            self.entry_materia_resumo.insert(0, valores[2]) 
            self.text_resumo.delete("1.0", "end")
            self.text_resumo.insert("1.0", valores[3]) 
            

            self.bt_confirmar_resumo.place(x=105, y=360)  
            
        except IndexError:
            messagebox.showerror("Erro", "Selecione uma linha na tabela.")
        except ValueError:
            messagebox.showerror("Erro", "Data inválida na linha selecionada.")
            
            
    def confirmar_atualizações_resumo(self):
        atualizar_resumo_treeview(self.tree, self.pegar_dados_resumo, self.exibir_tabela_resumos)

        self.bt_confirmar_resumo.place_forget()

        self.entry_data.entry.delete(0, END)  
        #self.entry_data_resumo.set_date(None)
        self.entry_materia_resumo.delete(0, END)
        self.text_resumo.delete("1.0", "end")


    def deletar_resumo(self):
        deletar_resumo_treeview(self.tree, self.exibir_tabela_resumos)       
    
    def pegar_dados_resumo(self):
        return [
            self.entry_data_resumo.entry.get(),
            self.entry_materia_resumo.get(),
            self.text_resumo.get("1.0", "end").strip()
        ]

    '''
        Funções para mostrar a tabela selecionada no frame:
    '''
        # Lado direito: Limpa e mostra as tabelas 
        # Lado esquerdo: Troca frames
        
    def exibir_tabela_anotações(self):     
        for widget in self.frame_direita_baixo_tabelas.winfo_children():
            widget.destroy()
        self.tree = mostrar_tabela_anotações(self.frame_direita_baixo_tabelas)
             
        self.frame_esquerda_semana.grid_remove()
        self.frame_esquerda_resumos.grid_remove()
        self.frame_esquerda_controle.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)

    def exibir_tabela_semana(self):
        for widget in self.frame_direita_baixo_tabelas.winfo_children():
            widget.destroy()
        self.tree = mostrar_tabela_semana(self.frame_direita_baixo_tabelas)

        self.frame_esquerda_controle.grid_remove()
        self.frame_esquerda_resumos.grid_remove()
        self.frame_esquerda_semana.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)

    def exibir_tabela_resumos(self):
        for widget in self.frame_direita_baixo_tabelas.winfo_children():
            widget.destroy()
        self.tree = mostrar_tabela_resumos(self.frame_direita_baixo_tabelas)
        
        self.frame_esquerda_controle.grid_remove()
        self.frame_esquerda_semana.grid_remove()
        self.frame_esquerda_resumos.grid(row=1, column=0, sticky='NSEW', padx=0, pady=1)