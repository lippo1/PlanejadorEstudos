import sqlite3
import pandas as pd
from tkinter import filedialog, messagebox
import openpyxl

class Exportador:
    def __init__(self, nome_banco="banco.db"):
        self.nome_banco = nome_banco

    def exportar_excel(self):
        try:
            conn = sqlite3.connect(self.nome_banco)
            query = "SELECT * FROM anotacoes"
            df = pd.read_sql_query(query, conn)
            conn.close()

            caminho = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                   filetypes=[("Arquivo Excel", "*.xlsx")])
            if not caminho:
                messagebox.showinfo("Cancelado", "Exportação cancelada.")
                return
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Exportado", "Dados exportados com sucesso para Excel!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")