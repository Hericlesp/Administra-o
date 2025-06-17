import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
import os

class RegistroFuncionario(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")
        self.master = master
        self.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuração do caminho do banco de dados
        self.DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
        self.DB_PATH = os.path.join(self.DB_DIR, 'database.db')
        
        self.conectar_banco()
        self.configurar_estilo()
        self.criar_interface()

    def conectar_banco(self):
        try:
            # Verificar se o diretório existe
            if not os.path.exists(self.DB_DIR):
                os.makedirs(self.DB_DIR)
                messagebox.showinfo("Info", f"Diretório criado: {self.DB_DIR}")
            
            self.conn = sqlite3.connect(self.DB_PATH)
            self.cursor = self.conn.cursor()
            
            # Verificar se a tabela existe
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='funcionarios'")
            if not self.cursor.fetchone():
                messagebox.showerror("Erro", "Tabela 'funcionarios' não encontrada no banco de dados!")
                return False
            
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Erro de Banco de Dados", f"Não foi possível conectar ao banco de dados:\n{str(e)}")
            return False
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado:\n{str(e)}")
            return False

    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#FFFFFF")
        style.configure("TLabel", background="#FFFFFF", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10), padding=5)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#e0e0e0")
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.map("Treeview", background=[('selected', '#4a6984')])
        style.configure("TLabelFrame", font=("Arial", 10, "bold"))

    def criar_interface(self):
        # Cabeçalho
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', pady=(0, 10))
        
        titulo = tk.Label(
            header_frame, 
            text="Consulta de Funcionários", 
            font=("Arial", 14, "bold"), 
            bg="white", 
            fg="#2c3e50"
        )
        titulo.pack(side='left')
        
        # Área de busca
        busca_frame = ttk.LabelFrame(self, text="Filtros de Busca")
        busca_frame.pack(fill='x', pady=10, ipady=5)
        
        ttk.Label(busca_frame, text="Buscar por:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.combo_filtro = ttk.Combobox(
            busca_frame, 
            values=["Matrícula", "Nome", "CPF", "Setor"], 
            state="readonly", 
            width=15
        )
        self.combo_filtro.grid(row=0, column=1, padx=5, pady=5)
        self.combo_filtro.current(1)  # Seleciona "Nome" por padrão
        
        self.entry_busca = ttk.Entry(busca_frame, width=40)
        self.entry_busca.grid(row=0, column=2, padx=5, pady=5, sticky='we')
        self.entry_busca.bind("<Return>", self.buscar_funcionarios)
        
        btn_buscar = ttk.Button(busca_frame, text="Buscar", command=self.buscar_funcionarios)
        btn_buscar.grid(row=0, column=3, padx=5, pady=5)
        
        btn_limpar = ttk.Button(busca_frame, text="Limpar", command=self.limpar_busca)
        btn_limpar.grid(row=0, column=4, padx=5, pady=5)
        
        busca_frame.columnconfigure(2, weight=1)

        # Tabela de resultados com barra de rolagem
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Criar Treeview com barra de rolagem
        scroll_y = ttk.Scrollbar(table_frame, orient='vertical')
        scroll_x = ttk.Scrollbar(table_frame, orient='horizontal')
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=("matricula", "nome", "setor"), 
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode='browse'
        )
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar colunas para a tabela funcionarios
        colunas = [
            ("matricula", "Matrícula", 100),
            ("nome", "Nome", 300),
            ("setor", "Setor", 150)
        ]
        
        for col_id, heading, width in colunas:
            self.tree.heading(col_id, text=heading)
            self.tree.column(col_id, width=width, anchor='center')
        
        # Layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        scroll_y.grid(row=0, column=1, sticky='ns')
        scroll_x.grid(row=1, column=0, sticky='ew')
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        self.tree.bind("<Double-1>", self.abrir_detalhes_funcionario)
        self.tree.bind("<Return>", self.abrir_detalhes_funcionario)
        
        # Status bar
        self.status_bar = ttk.Label(self, text="Pronto para buscar", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Carregar dados iniciais
        self.buscar_funcionarios()

    def limpar_busca(self):
        self.entry_busca.delete(0, tk.END)
        self.buscar_funcionarios()

    def buscar_funcionarios(self, event=None):
        filtro = self.combo_filtro.get()
        valor = self.entry_busca.get().strip()

        campo_map = {
            "Matrícula": "matricula_siape",
            "Nome": "nome_funcionario",
            "CPF": "cpf",
            "Setor": "lotacao"
        }
        campo = campo_map.get(filtro, "nome_funcionario")  # Default para nome

        try:
            if valor:
                # Usar parâmetros seguros para evitar SQL injection
                query = f"SELECT matricula_siape, nome_funcionario, lotacao FROM funcionarios WHERE {campo} LIKE ?"
                self.cursor.execute(query, (f"%{valor}%",))
            else:
                self.cursor.execute("SELECT matricula_siape, nome_funcionario, lotacao FROM funcionarios")

            resultados = self.cursor.fetchall()

            # Limpar treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Preencher com novos resultados
            for row in resultados:
                self.tree.insert("", "end", values=row)
                
            # Atualizar status
            self.status_bar.config(text=f"Encontrados {len(resultados)} funcionários")

        except sqlite3.Error as e:
            messagebox.showerror("Erro na Consulta", f"Erro ao buscar funcionários:\n{str(e)}")
            self.status_bar.config(text="Erro na consulta")

    def abrir_detalhes_funcionario(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        item = self.tree.item(selecionado[0])
        matricula = item['values'][0]

        try:
            self.cursor.execute("SELECT * FROM funcionarios WHERE matricula_siape = ?", (matricula,))
            dados = self.cursor.fetchone()
            
            if not dados:
                messagebox.showwarning("Não Encontrado", "Funcionário não encontrado no banco de dados!")
                return
                
            colunas = [desc[0] for desc in self.cursor.description]
            self.janela_detalhes(dict(zip(colunas, dados)))
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro na Consulta", f"Erro ao buscar detalhes do funcionário:\n{str(e)}")

    def janela_detalhes(self, dados):
        win = tk.Toplevel(self.master)
        win.title(f"Detalhes do Funcionário - {dados['nome_funcionario']}")
        win.geometry("700x600")
        win.transient(self.master)
        win.grab_set()
        win.resizable(True, True)

        # Frame principal com barra de rolagem
        main_frame = ttk.Frame(win)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Organizar campos em 2 colunas
        campos = [
            'matricula_siape', 'nome_funcionario', 'cargo', 'funcao', 'orgao', 'lotacao',
            'data_exercicio', 'tipo_contratacao', 'jornada_trabalho', 'telefone_corp', 'email_corp',
            'chefe_imediato', 'observacoes', 'nome_completo', 'nome_social', 'cpf', 'rg',
            'data_nascimento', 'estado_civil', 'naturalidade', 'nacionalidade', 'endereco_residencial',
            'telefone_pessoal', 'email_pessoal'
        ]
        
        self.entries_edicao = {}
        
        for i, chave in enumerate(campos):
            row = i // 2
            col = i % 2 * 2
            
            lbl = ttk.Label(scrollable_frame, text=f"{chave.replace('_', ' ').title()}:", 
                           font=("Arial", 10, "bold"))
            lbl.grid(row=row, column=col, sticky="e", padx=(10, 5), pady=5)
            
            valor = dados.get(chave, "") or ""  # Tratar valores None
            
            entry = ttk.Entry(scrollable_frame, width=35)
            entry.grid(row=row, column=col+1, sticky="we", padx=(0, 10), pady=5)
            entry.insert(0, valor)
            entry.config(state="readonly")
            self.entries_edicao[chave] = entry

        # Botões na parte inferior
        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Alterar Dados", 
                  command=self.habilitar_edicao).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Salvar", 
                  command=lambda: self.salvar_edicao(dados['matricula_siape'], win)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Exportar para CSV", 
                  command=lambda: self.exportar_para_csv(dados)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Fechar", 
                  command=win.destroy).pack(side='right', padx=5)

    def habilitar_edicao(self):
        for entry in self.entries_edicao.values():
            entry.config(state="normal")
            entry.config(background="#ffffcc")  # Destaque visual para campos editáveis

    def salvar_edicao(self, matricula, janela):
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja salvar as alterações?"):
            return
            
        try:
            dados_atualizados = {chave: entry.get() for chave, entry in self.entries_edicao.items()}
            campos = list(dados_atualizados.keys())
            valores = list(dados_atualizados.values())

            placeholders = ', '.join([f"{c} = ?" for c in campos])
            update_query = f"UPDATE funcionarios SET {placeholders} WHERE matricula_siape = ?"
            
            self.cursor.execute(update_query, (*valores, matricula))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            janela.destroy()
            self.buscar_funcionarios()  # Atualizar a lista
            
        except sqlite3.Error as e:
            messagebox.showerror("Erro na Atualização", f"Erro ao atualizar os dados:\n{str(e)}")

    def exportar_para_csv(self, dados):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
            initialfile=f"funcionario_{dados['matricula_siape']}.csv"
        )
        
        if not caminho:
            return
            
        try:
            with open(caminho, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=';')
                
                # Escrever cabeçalhos e dados
                writer.writerow(dados.keys())
                writer.writerow(dados.values())
                
            messagebox.showinfo("Exportado", f"Arquivo exportado com sucesso:\n{caminho}")
            
        except Exception as e:
            messagebox.showerror("Erro na Exportação", f"Erro ao exportar para CSV:\n{str(e)}")  
            
                      
if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroFuncionario(root)
    root.mainloop()