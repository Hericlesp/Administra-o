import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import random
import string
import json
import os

class SistemaCadastro:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Cadastro")
        self.master.geometry("900x600")
        
        # Carregar dados
        self.dados_funcionarios = self.carregar_dados()
        self.horarios_config = self.carregar_horarios()
        
        # Criar abas principais
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)
        
        # Abas existentes
        self.abas = {
            "dados_pessoais": ttk.Frame(self.notebook),
            "documentos": ttk.Frame(self.notebook),
            "endereco": ttk.Frame(self.notebook),
            "caracteristicas": ttk.Frame(self.notebook),
            "estrangeiro": ttk.Frame(self.notebook),
            "dependentes": ttk.Frame(self.notebook),
            "codigo_ponto": ttk.Frame(self.notebook),
            "config_horarios": ttk.Frame(self.notebook)
        }
        
        # Adicionar abas
        for nome, frame in self.abas.items():
            self.notebook.add(frame, text=nome.replace('_', ' ').title())
        
        # Criar conteúdo das abas
        self.criar_aba_dados_pessoais()
        self.criar_aba_documentos()
        self.criar_aba_endereco()
        self.criar_aba_caracteristicas()
        self.criar_aba_estrangeiro()
        self.criar_aba_dependentes()
        self.criar_aba_codigo_ponto()
        self.criar_aba_config_horarios()
        
        # Botão de salvar
        ttk.Button(master, text="Salvar Tudo", command=self.salvar_tudo).pack(pady=10)

    # Métodos de carregamento/salvamento (igual ao anterior)
    def carregar_dados(self):
        try:
            if os.path.exists("funcionarios.json"):
                with open("funcionarios.json", "r") as f:
                    return json.load(f)
        except:
            return {}

    def salvar_dados(self):
        with open("funcionarios.json", "w") as f:
            json.dump(self.dados_funcionarios, f, indent=2)

    # ... (métodos das abas existentes mantidos iguais)

    def criar_aba_codigo_ponto(self):
        frame = self.abas["codigo_ponto"]
        
        # Widgets da aba de código
        ttk.Label(frame, text="Gerador de Código Único").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Seleção de funcionário
        ttk.Label(frame, text="Funcionário:").grid(row=1, column=0, sticky='e')
        self.cb_funcionarios = ttk.Combobox(frame, values=self.listar_funcionarios())
        self.cb_funcionarios.grid(row=1, column=1, pady=5, sticky='we')
        
        # Código gerado
        self.codigo_var = tk.StringVar(value="Clique em Gerar")
        ttk.Label(frame, text="Código:").grid(row=2, column=0, sticky='e')
        ttk.Label(frame, textvariable=self.codigo_var, font=('Arial', 12)).grid(row=2, column=1, sticky='w')
        
        # Botões
        ttk.Button(frame, text="Gerar Código", command=self.gerar_codigo).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Salvar Código", command=self.salvar_codigo).grid(row=3, column=1, pady=10)

    def criar_aba_config_horarios(self):
        frame = self.abas["config_horarios"]
        
        # Widgets de configuração
        ttk.Label(frame, text="Configuração de Horários").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Seleção de funcionário
        ttk.Label(frame, text="Funcionário:").grid(row=1, column=0, sticky='e')
        self.cb_func_horarios = ttk.Combobox(frame, values=self.listar_funcionarios())
        self.cb_func_horarios.grid(row=1, column=1, pady=5, sticky='we')
        
        # Campos de horário
        horarios = ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída", "Hora Extra"]
        self.entries_horarios = {}
        
        for i, horario in enumerate(horarios):
            ttk.Label(frame, text=f"{horario}:").grid(row=i+2, column=0, sticky='e')
            entry = ttk.Entry(frame, width=10)
            entry.grid(row=i+2, column=1, pady=2, sticky='w')
            self.entries_horarios[horario.lower()] = entry
        
        # Botões
        ttk.Button(frame, text="Salvar Horários", command=self.salvar_horarios).grid(row=len(horarios)+2, column=0, columnspan=2, pady=10)

    # ... (implementar os métodos restantes)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaCadastro(root)
    root.mainloop()