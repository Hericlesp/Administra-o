# pages/admin/empresa/registro_empresa.py
import tkinter as tk
from tkinter import ttk, messagebox
from DATABESE.DATABASE import criar_banco_e_tabelas
# from pages.admin.empresa.consulta_empresas import ConsultaEmpresas
import os
import sqlite3

# Cria o banco (apenas na primeira vez)
# criar_banco()

DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

class RegistroEmpresa(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.dados_empresa()

    def dados_empresa(self):
        self.grid_columnconfigure(0, weight=1)

        frame_destaque = tk.Frame(self, bg='#FF4500')
        frame_destaque.grid(row=0, column=0, columnspan=3, sticky='ew')

        label_principal = tk.Label(frame_destaque, text='CADASTRAR EMPRESA',
                                   fg="#FFFFFF", bg="#FF4500", font=("Arial", 14, "bold"))
        label_principal.pack(anchor='center')

        cadastro = ttk.Notebook(self)
        cadastro.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)
        aba1 = tk.Frame(cadastro, bg="#FFFFFF")
        aba2 = tk.Frame(cadastro, bg="#FFFFFF")
        aba3 = tk.Frame(cadastro, bg="#FFFFFF")

        cadastro.add(aba1, text='Dados da empresa')
        cadastro.add(aba2, text='Responsável')
        cadastro.add(aba3, text='Acesso e Controle Interno')

        campos_aba1 = [
            "Razão Social", "Nome Fantasia", "CNPJ", "Inscrição Municipal",
            "Natureza Jurídica", "Ramo de Atividade", "Data de Fundação",
            "Endereço", "CEP", "País",
            "Telefone Fixo", "Telefone Celular / WhatsApp", "E-mail Corporativo"
        ]
        self.entradas = {}
        for i, campo in enumerate(campos_aba1):
            tk.Label(aba1, text=campo, bg='#FFFFFF', anchor='w').grid(row=i, column=0, sticky='w', padx=5, pady=3)
            entry = tk.Entry(aba1, width=50, bg='#FFFFFF')
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.entradas[campo] = entry

        campos_aba2 = [
            "Nome Completo", "Cargo", "CPF", "RG",
            "E-mail do responsável", "Telefone do responsável"
        ]
        self.responsavel = {}
        for i, campo in enumerate(campos_aba2):
            tk.Label(aba2, text=campo, bg='#FFFFFF', anchor='w').grid(row=i, column=0, sticky='w', padx=5, pady=3)
            entry = tk.Entry(aba2, width=50, bg='#FFFFFF')
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.responsavel[campo] = entry

        campos_aba3 = ["Usuário administrador", "Nível de acesso permitido"]
        self.acesso = {}
        for i, campo in enumerate(campos_aba3):
            tk.Label(aba3, text=campo, bg='#FFFFFF', anchor='w').grid(row=i, column=0, sticky='w', padx=5, pady=3)
            entry = tk.Entry(aba3, width=50, bg='#FFFFFF')
            entry.grid(row=i, column=1, padx=5, pady=3)
            self.acesso[campo] = entry

        salvar = tk.Button(
            self, text="SALVAR DADOS", fg="#FFFFFF", bg="#FF4500", width=20,
            font=("Arial", 10, "bold"), command=self.salvar_dados
        )
        salvar.grid(row=3, column=0, pady=10, sticky='w')

        botao_consultar = tk.Button(
            self, text="CONSULTAR EMPRESA", fg="#FFFFFF", bg="#FF4500", width=20,
            font=("Arial", 10, "bold"), command=self.abrir_consulta)
        botao_consultar.grid(row=3, column=1, pady=10, sticky='e')

    # def abrir_consulta(self):
    #     ConsultaEmpresas(self)

    def salvar_dados(self):
        dados_empresa = {k: v.get() for k, v in self.entradas.items()}
        dados_resp = {k: v.get() for k, v in self.responsavel.items()}
        dados_acesso = {k: v.get() for k, v in self.acesso.items()}

        if not dados_empresa["Razão Social"] or not dados_empresa["CNPJ"]:
            messagebox.showwarning("Atenção", "Preencha pelo menos a Razão Social e o CNPJ.")
            return

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # conexao = conectar()
            # cursor = conexao.cursor()

            cursor.execute("""
                INSERT INTO empresas (
                    razao_social, nome_fantasia, cnpj, inscricao_municipal,
                    natureza_juridica, ramo_atividade, data_fundacao,
                    endereco, cep, pais,
                    telefone_fixo, telefone_celular, email_corporativo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                dados_empresa["Razão Social"], dados_empresa["Nome Fantasia"], dados_empresa["CNPJ"],
                dados_empresa["Inscrição Municipal"], dados_empresa["Natureza Jurídica"],
                dados_empresa["Ramo de Atividade"], dados_empresa["Data de Fundação"],
                dados_empresa["Endereço"], dados_empresa["CEP"], dados_empresa["País"],
                dados_empresa["Telefone Fixo"], dados_empresa["Telefone Celular / WhatsApp"],
                dados_empresa["E-mail Corporativo"]
            ))

            empresa_id = cursor.lastrowid

            cursor.execute("""
                INSERT INTO responsaveis (
                    empresa_id, nome_completo, cargo, cpf, rg, email, telefone
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                empresa_id, dados_resp["Nome Completo"], dados_resp["Cargo"],
                dados_resp["CPF"], dados_resp["RG"], dados_resp["E-mail do responsável"],
                dados_resp["Telefone do responsável"]
            ))

            cursor.execute("""
                INSERT INTO acessos (
                    empresa_id, usuario_admin, nivel_acesso
                ) VALUES (?, ?, ?)
            """, (
                empresa_id, dados_acesso["Usuário administrador"], dados_acesso["Nível de acesso permitido"]
            ))

            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Empresa cadastrada com sucesso!")

            for dicionario in [self.entradas, self.responsavel, self.acesso]:
                for campo in dicionario.values():
                    campo.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar os dados: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Cadastro de Empresa")
    root.geometry("800x600")
    app = RegistroEmpresa(master=root)
    app.mainloop()