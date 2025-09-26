import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
from database import pegar_caminho_do_banco_de_dados, pegar_dados_semana, pegar_dados_resumo 

class Exportador:
    def __init__(self):
        self.nome_banco = pegar_caminho_do_banco_de_dados()  # Usa o caminho local

    def exportar_anotacoes(self):  
        try:
            conn = sqlite3.connect(self.nome_banco)
            query = "SELECT * FROM anotacoes"
            df = pd.read_sql_query(query, conn)
            conn.close()

            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Arquivo Excel", "*.xlsx")],
                                                   title="Exportar Anotações")
            if not caminho:
                messagebox.showinfo("Cancelado", "Exportação cancelada.")
                return
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Exportado", "Anotações exportadas com sucesso para Excel!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar anotações: {str(e)}")


    def exportar_semana(self):
        try:
            data = pegar_dados_semana()  
            if not data:
                messagebox.showinfo("Sem Dados", "Não há dados na tabela de semana.")
                return
     
            df = pd.DataFrame([data[0]], columns=['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado'])
            
            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Arquivo Excel", "*.xlsx")],
                                                   title="Exportar Semana")
            if not caminho:
                messagebox.showinfo("Cancelado", "Exportação cancelada.")
                return
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Exportado", "Semana exportada com sucesso para Excel!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar semana: {str(e)}")

  
    def exportar_resumos(self):
        try:
            data = pegar_dados_resumo()  
            if not data:
                messagebox.showinfo("Sem Dados", "Não há dados na tabela de resumos.")
                return
            df = pd.DataFrame(data, columns=['ID', 'Data', 'Matéria', 'Resumo'])
            
            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Arquivo Excel", "*.xlsx")],
                                                   title="Exportar Resumos")
            if not caminho:
                messagebox.showinfo("Cancelado", "Exportação cancelada.")
                return
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Exportado", "Resumos exportados com sucesso para Excel!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar resumos: {str(e)}")