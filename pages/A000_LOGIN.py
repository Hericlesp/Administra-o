import tkinter as tk
from tkinter import messagebox
import sqlite3
import os
import importlib

# 🔗 Caminho do banco
DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

# # 🔗 Caminho do banco
# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')

# 🧠 Seus módulos
import pages.A00_MAIN as main
import pages.A006_PONTO_DO_USUARIO as USER_ponto_user_main


class LoginSistema:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Ponto")
        self.root.geometry("500x350")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.usuario_var = tk.StringVar()
        self.senha_var = tk.StringVar()

        self.criar_widgets()
        

    def criar_widgets(self):
        self.top_frame = tk.Frame(self.root, bg="#F09001", height=80)
        self.top_frame.pack(fill="x")

        tk.Label(
            self.top_frame, text="Acesso ao Sistema",
            font=("Arial", 20, "bold"), bg="#F09001", fg="black"
        ).pack(pady=20)

        self.center_frame = tk.Frame(self.root, bg="white")
        self.center_frame.pack(pady=20)

        tk.Label(
            self.center_frame, text="RA (Usuário):",
            font=("Arial", 14, "bold"), bg="white", fg="black"
        ).grid(row=0, column=0, sticky="e", padx=10, pady=10)

        self.usuario_entry = tk.Entry(
            self.center_frame, textvariable=self.usuario_var,
            font=("Arial", 14), bg="#f0f0f0", width=25
        )
        self.usuario_entry.grid(row=0, column=1, pady=10)

        tk.Label(
            self.center_frame, text="Senha:",
            font=("Arial", 14, "bold"), bg="white", fg="black"
        ).grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.senha_entry = tk.Entry(
            self.center_frame, textvariable=self.senha_var,
            show="*", font=("Arial", 14), bg="#f0f0f0", width=25
        )
        self.senha_entry.grid(row=1, column=1, pady=10)

        self.login_btn = tk.Button(
            self.center_frame, text="Entrar",
            font=("Arial", 14, "bold"), bg="#0300A7", fg="white",
            width=20, command=self.fazer_login
        )
        self.login_btn.grid(row=2, column=0, columnspan=2, pady=20)
        

    def fazer_login(self):
        matricula = self.usuario_var.get().strip()
        senha = self.senha_var.get().strip()

        if not matricula or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return
        
        try:
            matricula_int = int(matricula)  # Convertendo para inteiro
            
        except ValueError:
            messagebox.showerror("Erro", "Matrícula deve ser numérica.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT cargo FROM Usuarios WHERE matricula = ? AND senha = ?",
            (matricula_int, senha)
        )
        resultado = cursor.fetchone()
        conn.close()

    
        if resultado:
            cargo = resultado[0]
            messagebox.showinfo("Login", f"Bem-vindo, {cargo.upper()}!")

            self.root.destroy()  # Fecha a janela de login

               
            if cargo in ["ROOT", "ADM"]:
                novo_root = tk.Tk()
                main.SistemaPonto(novo_root).run()

                
            elif cargo == "USER":
                novo_root = tk.Tk()
                USER_ponto_user_main.SistemaPonto(novo_root, matricula_int).run()

            else:
                messagebox.showerror("Erro", "Permissão desconhecida!")

        else:
            messagebox.showerror("Erro", "Matrícula ou senha incorretos.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSistema(root)
    root.mainloop()
