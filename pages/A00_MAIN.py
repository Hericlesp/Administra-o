import tkinter as tk
import sqlite3
import os

import pages.A01_CADASTRAR_FUNCIONARIO as registro_funcionario
import pages.A02_STATUS_DO_DIA as point

import pages.A04_HELP as help
import pages.A07_CONSULTA_FUNCIONARIO as cf

from DATABESE.DATABASE import criar_banco_e_tabelas
from pages.registro_empresa import RegistroEmpresa


DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')

class SistemaPonto:

    #@staticmethod
    # def criar_banco():
    #     if not os.path.exists(DB_DIR):
    #         os.makedirs(DB_DIR)

    #     conn = sqlite3.connect(DB_PATH)
    #     cursor = conn.cursor()

    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS Colaborador (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             RA INTEGER UNIQUE,
    #             Nome TEXT NOT NULL,
    #             Setor TEXT,
    #             Email TEXT,
    #             Celular TEXT,
    #             Codigo TEXT NOT NULL
    #         )
    #     ''')

    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS RegistroPonto (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             id_funcionario INTEGER,
    #             data TEXT,
    #             hora TEXT,
    #             tipo TEXT,
    #             FOREIGN KEY (id_funcionario) REFERENCES Colaborador(id)
    #         )
    #     ''')

        # conn.commit()
        # conn.close()
        # print('🗄️ Banco de dados verificado/criado com sucesso!')

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Ponto - ADMIN")
        self.root.geometry("1000x800")
        self.root.minsize(1300, 1000)
        self.root.configure(bg="white")

        # Variável para controlar se o gerador de código está aberto
        self.gerador_codigo_aberto = False

        self.criar_widgets()

    def criar_widgets(self):
        self.top_frame = tk.Frame(self.root, bg="green", height=70)
        self.top_frame.pack(fill="x", side="top")

        self.title_lbl = tk.Label(
            self.top_frame, text="REGISTRO \n DE PONTO - ADMIN",
            font=("Arial", 20, "bold"), bg="green", fg="white"
        )
        self.title_lbl.pack(padx=10, pady=15)

        self.menu_frame = tk.Frame(self.root, bg="#d9d9d9", width=150)
        self.menu_frame.pack(fill="y", side="left")

        # Botões do menu lateral
        
        self.btn_consulta = tk.Button(
            self.menu_frame, text="🔍 | Consulta", bg="#f0f0f0", width=15,
            command=self.abrir_consulta
        )
        self.btn_consulta.pack(pady=10)
        
        
        self.btn_cadastro = tk.Button(
            self.menu_frame, text="✏️ | Cadastro", bg="#f0f0f0", width=15,
            command=self.abrir_cadastro
        )
        self.btn_cadastro.pack(pady=10)

        # self.btn_gerar = tk.Button(
        #     self.menu_frame,
        #     text=" 🔢 | Gerar Código",
        #     bg="#f0f0f0",
        #     width=15,
        #     command=self.abrir_gerador_codigo
        # )
        # self.btn_gerar.pack(pady=10)

        self.btn_registrar = tk.Button(
            self.menu_frame, text="📋 | Status do Dia", bg="#f0f0f0", width=15,
            command=self.abrir_ponto
        )
        self.btn_registrar.pack(pady=10)
        
        botao_empresa = tk.Button(self.menu_frame, text="🏢 | Cadastrar Empresa", command=self.abrir_registro_empresa, bg="#FF4500", fg="white")
        botao_empresa.pack(pady=5, fill='x')


        self.btn_help = tk.Button(
            self.menu_frame,
            text="🛟 | Help",
            bg="#f0f0f0",
            width=15,
            command=lambda: help.infohelp(self.center_frame)
        )
        self.btn_help.pack(pady=10)

        self.btn_sair = tk.Button(
            self.menu_frame, text="🚪 | Sair", bg="#f0f0f0", width=15,
            command=self.root.quit
        )
        self.btn_sair.pack(pady=10)

        self.center_frame = tk.Frame(self.root, bg="white")
        self.center_frame.pack(fill="both", side="left", expand=True, padx=25, pady=15)

        self.abrir_home()

    # def abrir_gerador_codigo(self):
    #     if self.gerador_codigo_aberto:
    #         # Se já aberto, não abre outro
    #         return

    #     self.gerador_codigo_aberto = True
    #     # Desabilita botões cadastro e help, mantém status do dia habilitado
    #     self.btn_cadastro.config(state="disabled")
    #     self.btn_gerar.config(state="disabled")
    #     self.btn_help.config(state="disabled")

    #     # Cria a janela do gerador de código
    #     janela_gerador = gerador_de_codigo.TelaGerarCodigo(self.root)

    #     def on_fechar():
    #         self.gerador_codigo_aberto = False
    #         # Reabilita os botões quando a janela for fechada
    #         self.btn_cadastro.config(state="normal")
    #         self.btn_gerar.config(state="normal")
    #         self.btn_help.config(state="normal")
    #         janela_gerador.janela.destroy()

    #     # Substitui o botão fechar da janela gerador para controlar o estado
    #     janela_gerador.janela.protocol("WM_DELETE_WINDOW", on_fechar)

    def limpar_center(self):
        for widget in self.center_frame.winfo_children():
            widget.destroy()

    def abrir_cadastro(self):
        self.limpar_center()
        registro_funcionario.RegistroFuncionario(self.center_frame)

    def abrir_ponto(self):
        self.limpar_center()
        point.Point(self.center_frame)
        
    def abrir_registro_empresa(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()
        RegistroEmpresa(self.frame_conteudo)

    def abrir_home(self):
        self.limpar_center()
        tk.Label(
            self.center_frame, text="Bem-vindo ao Sistema de Registro de Ponto - ADMIN",
            font=("Arial", 18, "bold"), bg="white"
        ).pack(pady=50)
        
    def abrir_consulta(self):
        self.limpar_center()
        cf.RegistroFuncionario(self.center_frame)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    criar_banco_e_tabelas()
    root = tk.Tk()
    app = SistemaPonto(root)
    app.run()
