import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import datetime as dt

DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')


class SistemaPonto:
    def __init__(self, root,matricula_usuario = None):
        self.root = root
        self.root.title("Registro de ponto")
        self.root.geometry("450x450")
        self.root.minsize(450, 450)
        self.root.resizable(False, True)
        self.root.configure(bg="white")

        self.nome_var = tk.StringVar()
        self.ra_var = tk.StringVar()
        self.codigo_var = tk.StringVar()
        self.tipo_var = tk.StringVar()

        self.funcionario_id = None
        self.matricula_usuario = matricula_usuario  # Armazena a matrícula como atributo

        self.criar_widgets()
        self.carregar_dados_usuario()  # Carrega o funcionário exemplo na inicialização

    def criar_widgets(self):
        self.top_frame = tk.Frame(self.root, bg="#F09001", width=900, height=100)
        self.top_frame.pack(fill="x", side="top")

        self.title_lbl = tk.Label(
            self.top_frame, text="Ponto Eletrônico",
            font=("Arial", 20, "bold"), bg="#F09001", fg="black"
        )
        self.title_lbl.pack(padx=10, pady=10)

        self.center_frame = tk.Frame(self.root, bg="white")
        self.center_frame.pack(fill="both", side="top", padx=0, pady=15)

        self.nome_lbl = tk.Label(
            self.center_frame, textvariable=self.nome_var,
            font=("Arial", 20, "bold"), bg="white", fg="black"
        )
        self.nome_lbl.pack(padx=10)

        self.matricula_lbl = tk.Label(
            self.center_frame, textvariable=self.ra_var,
            font=("Arial", 14), bg="white", fg="black"
        )
        self.matricula_lbl.pack(padx=10)

        tk.Label(
            self.center_frame, text="CÓDIGO",
            font=("Arial", 14, "bold"), bg="white", fg="black"
        ).pack(padx=10, pady=10)

        self.codigo_ety = tk.Entry(
            self.center_frame, font=("Arial", 20, "bold"),
            bg="#f0f0f0", fg="black", width=15, justify="center"
        )
        self.codigo_ety.pack(pady=5)

        buscar_btn = tk.Button(
            self.center_frame, text="Buscar",
            font=("Arial", 10), bg="#F09001", fg="black",
            command=self.buscar_funcionario
        )
        buscar_btn.pack(pady=5)

        tk.Label(
            self.center_frame, text="Tipo de Registro",
            font=("Arial", 14), bg="white", fg="black"
        ).pack(pady=5)

        self.tipo_cbx = ttk.Combobox(
            self.center_frame, values=["Entrada", "Almoço", "Retorno", "Saída"],
            font=("Arial", 12), state="readonly", textvariable=self.tipo_var
        )
        self.tipo_cbx.pack(pady=5)
        self.tipo_cbx.set("Entrada")

        self.footer_frame = tk.Frame(self.root, bg="white")
        self.footer_frame.pack(fill="both", pady=10)

        registrar_btn = tk.Button(
            self.footer_frame, text="Registrar",
            font=("Arial", 14), bg="#0300A7", fg="white",
            width=20, height=2, command=self.registrar_ponto
        )
        registrar_btn.pack(pady=10)
        
        
        
#----------------------------------------------------------------------------------------------




    def carregar_dados_usuario(self):
        """Carrega os dados do usuário logado usando a matrícula"""
        print(f"DEBUG: Matrícula recebida = {self.matricula_usuario}")  # Adicione esta linha
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Busca dados na tabela cadastros (funcionários)
            cursor.execute(
                "SELECT id, nome, matricula FROM cadastros WHERE matricula = ?", 
                (self.matricula_usuario,)  # CORREÇÃO: adicione a vírgula aqui
            )
            resultado = cursor.fetchone()
            
            if resultado:
                self.funcionario_id = resultado[0]
                self.nome_var.set(resultado[1])
                self.ra_var.set(f"MATRÍCULA: {resultado[2]}")
            else:
                # Se não encontrou na tabela de cadastros, tenta na tabela de usuários
                cursor.execute(
                    "SELECT matricula, cargo FROM usuarios WHERE matricula = ?", 
                    (self.matricula_usuario,)
                )
                resultado_usuario = cursor.fetchone()
                
                if resultado_usuario:
                    self.nome_var.set(f"Usuário ({resultado_usuario[1]})")
                    self.ra_var.set(f"MATRÍCULA: {resultado_usuario[0]}")
                    # Para usuários que não são funcionários, não temos ID de funcionário
                    self.funcionario_id = None
                else:
                    messagebox.showerror("Erro", "Usuário não encontrado!")
                    self.funcionario_id = None
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Ocorreu um erro: {e}")
        finally:
            conn.close()
            
        
    def buscar_funcionario(self):
        """Busca funcionário por código (agora usando a nova estrutura de banco)"""
        codigo = self.codigo_ety.get().strip()

        if not codigo:
            messagebox.showwarning("Aviso", "Digite o código!")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Busca na tabela de códigos
        cursor.execute(
            "SELECT colaborador_id, tipo, status FROM registros_codigos WHERE codigo = ? AND status = 'Ativo'",
            (codigo,)
        )
        codigo_resultado = cursor.fetchone()
        
        if codigo_resultado:
            colaborador_id = codigo_resultado[0]
            tipo_codigo = codigo_resultado[1]
            
            # Busca dados do colaborador
            cursor.execute(
                "SELECT id, nome, matricula FROM cadastros WHERE id = ?", 
                (colaborador_id,)
            )
            resultado = cursor.fetchone()
            
            if resultado:
                self.funcionario_id = resultado[0]
                self.nome_var.set(resultado[1])
                self.ra_var.set(f"MATRÍCULA: {resultado[2]}")
                self.tipo_cbx.set(tipo_codigo)  # Define o tipo automaticamente
            else:
                messagebox.showerror("Erro", "Colaborador não encontrado!")
        else:
            messagebox.showerror("Erro", "Código inválido ou expirado!")
        
        conn.close()

    def registrar_ponto(self):
        if not self.funcionario_id:
            messagebox.showerror("Erro", "Busque um funcionário antes de registrar.")
            return

        tipo = self.tipo_var.get()
        data = dt.datetime.now().strftime('%Y-%m-%d')
        hora = dt.datetime.now().strftime('%H:%M:%S')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Registra o ponto
        cursor.execute(
            '''
            INSERT INTO registro_ponto (colaborador_id, data, hora, tipo)
            VALUES (?, ?, ?, ?)
            ''',
            (self.funcionario_id, data, hora, tipo)
        )
        
        # Atualiza o status do código para expirado
        codigo = self.codigo_ety.get().strip()
        if codigo:
            cursor.execute(
                "UPDATE registros_codigos SET status = 'Expirado' WHERE codigo = ?",
                (codigo,)
            )

        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"{tipo} registrado com sucesso!")
        # Limpa o campo de código após o registro
        self.codigo_ety.delete(0, tk.END)
        
        
    def run(self):
        self.root.mainloop()


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

#     cursor.execute(
#         "SELECT * FROM Colaborador WHERE RA = ?", (998096,)
#     )
#     if cursor.fetchone() is None:
#         cursor.execute(
#             '''
#             INSERT INTO Colaborador (RA, Nome, Setor, Email, Celular, Codigo)
#             VALUES (?, ?, ?, ?, ?, ?)
#             ''',
#             (
#                 998096,
#                 'Hericles Paulo da Silva Mendes',
#                 'TI',
#                 'hericles@email.com',
#                 '11999999999',
#                 '1234'
#             )
#         )
#         print("Funcionário exemplo cadastrado com sucesso!")

#     conn.commit()
#     conn.close()


if __name__ == "__main__":
    # criar_banco()
    root = tk.Tk()
    app = SistemaPonto(root)
    app.run()
