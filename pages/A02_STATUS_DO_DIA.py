import tkinter as tk
import sqlite3
import os
from datetime import datetime

DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')  # banco correto

# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')  # banco correto

class Point:

    def __init__(self, master):
        self.master = master
        self.master.configure(bg="white")

        self.data_hoje = datetime.now().strftime('%Y-%m-%d')

        self.titulo = tk.Label(
            master, text="STATUS DO DIA", font=("Arial", 20, "bold"), bg="white"
        )
        self.titulo.pack(pady=10)

        self.frame_info = tk.Frame(master, bg="white")
        self.frame_info.pack(pady=10)

        self.label_total = tk.Label(self.frame_info, text="", bg="white", font=("Arial", 12))
        self.label_total.grid(row=0, column=0, padx=20)

        self.label_registrados = tk.Label(self.frame_info, text="", bg="white", fg="green", font=("Arial", 12))
        self.label_registrados.grid(row=0, column=1, padx=20)

        self.label_pendentes = tk.Label(self.frame_info, text="", bg="white", fg="red", font=("Arial", 12))
        self.label_pendentes.grid(row=0, column=2, padx=20)

        self.frame_listas = tk.Frame(master, bg="white")
        self.frame_listas.pack(pady=10, fill="both", expand=True)

        # Listas
        self.frame_left = tk.Frame(self.frame_listas, bg="#f0f0f0", bd=2, relief="groove")
        self.frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        self.frame_right = tk.Frame(self.frame_listas, bg="#f0f0f0", bd=2, relief="groove")
        self.frame_right.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        tk.Label(
            self.frame_left, text="✅ Já Registraram Hoje", bg="#f0f0f0",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        self.lista_registrados = tk.Listbox(self.frame_left, width=40, height=20)
        self.lista_registrados.pack(padx=10, pady=10, fill="both", expand=True)

        tk.Label(
            self.frame_right, text="❌ Não Registraram Hoje", bg="#f0f0f0",
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        self.lista_pendentes = tk.Listbox(self.frame_right, width=40, height=20)
        self.lista_pendentes.pack(padx=10, pady=10, fill="both", expand=True)

        # Atualiza os dados pela primeira vez
        self.carregar_dados()

        # Agenda atualização periódica
        self.atualizar_periodicamente()

    def carregar_dados(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Buscar todos os colaboradores no banco correto e com colunas corretas
        cursor.execute("SELECT id, nome, matricula FROM cadastros WHERE ativo='Sim'")
        colaboradores = cursor.fetchall()

        total = len(colaboradores)
        registrados = []
        pendentes = []

        for colaborador in colaboradores:
            colaborador_id, nome, matricula = colaborador

            cursor.execute('''
                SELECT COUNT(*) FROM registro_ponto
                WHERE colaborador_id = ? AND data = ?
            ''', (colaborador_id, self.data_hoje))

            resultado = cursor.fetchone()
            if resultado and resultado[0] > 0:
                registrados.append(f"{nome} | Matrícula: {matricula}")
            else:
                pendentes.append(f"{nome} | Matrícula: {matricula}")

        conn.close()

        # Atualiza listas
        self.lista_registrados.delete(0, tk.END)
        self.lista_pendentes.delete(0, tk.END)

        for nome in registrados:
            self.lista_registrados.insert(tk.END, nome)

        for nome in pendentes:
            self.lista_pendentes.insert(tk.END, nome)

        # Atualiza contagens
        self.label_total.config(text=f"👥 Total: {total}")
        self.label_registrados.config(text=f"✅ Registraram: {len(registrados)}")
        self.label_pendentes.config(text=f"❌ Pendentes: {len(pendentes)}")

    def atualizar_periodicamente(self):
        self.data_hoje = datetime.now().strftime('%Y-%m-%d')  # Atualiza a data hoje (caso rode após meia-noite)
        self.carregar_dados()
        # Atualiza a cada 2 segundos (2000 milissegundos)
        self.master.after(2000, self.atualizar_periodicamente)


if __name__ == "__main__":
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    root = tk.Tk()
    app = Point(root)
    root.title("Registro de Ponto")
    root.geometry("800x600")
    root.mainloop()
