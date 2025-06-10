import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sqlite3
import pandas as pd  

class EstatisticasJanela:
    def __init__(self, root):
        self.root = root
        self.root.title("Estatísticas de Estudos")

        # --- Combobox ---
        ttk.Label(self.root, text="Escolha a Matéria:").pack(pady=5)
        self.combo = ttk.Combobox(self.root, state="readonly")
        self.combo.pack()

        # --- Botão ---
        self.botao = ttk.Button(self.root, text="Gerar Gráfico", command=self.gerar_grafico)
        self.botao.pack(pady=5)

        # --- Frame para o gráfico ---
        self.frame_grafico = tk.Frame(self.root)
        self.frame_grafico.pack()
        self.canvas = None  # Para controlar o gráfico atual

        # Carregar matérias
        self.carregar_materias()

    def carregar_materias(self):
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT materia FROM anotacoes")
        materias = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.combo['values'] = materias
        if materias:
            self.combo.set(materias[0])

    def gerar_grafico(self):
        materia = self.combo.get()
        if not materia:
            return

        # Obter dados do banco via pandas
        conn = sqlite3.connect("banco.db")
        df = pd.read_sql_query(
            "SELECT assunto, minutos FROM anotacoes WHERE materia = ?",
            conn,
            params=(materia,)
        )
        conn.close()

        if df.empty:
            return

        # Agrupar por assunto e somar os minutos
        df_agrupado = df.groupby("assunto", as_index=False)["minutos"].sum()

        # Destruir gráfico anterior (se houver)
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        # Criar novo gráfico
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_agrupado["assunto"], df_agrupado["minutos"], color='skyblue')
        ax.set_title(f"Minutos por Assunto - {materia}")
        ax.set_ylabel("Minutos")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_grafico)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = EstatisticasJanela(root)
    root.mainloop()
