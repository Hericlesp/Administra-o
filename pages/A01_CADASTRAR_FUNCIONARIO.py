import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import random
import string
import json
import os


class RegistroFuncionario(tk.Frame):
     #----------------------------------------------------------
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.pack(fill="both", expand=True)

        self.conectar_banco()
        self.criar_tabela()

        # Carregar dados existentes
        self.dados_funcionarios = self.carregar_dados()
        self.horarios_config = self.carregar_horarios()
        self.registros_ponto = self.carregar_registros()

        # Criar interface primeiro (define self.aba_codigo_ponto e self.aba_config_horarios)
        self.criar_interface()

        # Criar abas
        # self.abas = {
        #      "codigo_ponto": ttk.Frame(self.notebook),
        #      "config_horarios": ttk.Frame(self.notebook),

        #  }


        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TNotebook", background="#e0e0e0")
        self.style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=(10, 5))
        self.style.configure("Header.TLabel", font=("Arial", 12, "bold"), foreground="#2c3e50")

        # Botões de ação
        btn_frame = ttk.Frame(self.master)
        btn_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(btn_frame, text="Salvar Dados", command=self.salvar_tudo).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Limpar Tudo", command=self.limpar_tudo).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Sair", command=self.sair).pack(side='right', padx=5)

  
  #-----------------------------------------------------------
        
    def conectar_banco(self):
        self.conn = sqlite3.connect(r'C:\Users\998096\Documents\python\Administração\DATA\database.db')
        self.cursor = self.conn.cursor()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula INTEGER UNIQUE NOT NULL,
                contato INTEGER,
                idade INTEGER,
                data_nascimento TEXT,
                cpf INTEGER,
                rg INTEGER,
                tipo_contratacao TEXT CHECK (tipo_contratacao IN ('Fixa', 'Horista')),
                cargo TEXT CHECK (cargo IN ('ADM', 'USER')),
                salario REAL,
                data_admissao TEXT,
                ativo TEXT CHECK (ativo IN ('Sim', 'Não')) DEFAULT 'Sim',
                
                -- Novos campos adicionados
                filiacao_mae TEXT,
                filiacao_pai TEXT,
                local_nascimento TEXT,
                nacionalidade TEXT,
                uf_nascimento TEXT,
                estado_civil TEXT,
                conjuge TEXT,
                certidao_casamento TEXT,
                rg_emissao TEXT,
                rg_orgao_emissor TEXT,
                rg_data_emissao TEXT,
                cart_profissional TEXT,
                conselho TEXT,
                ctps TEXT,
                ctps_serie TEXT,
                cart_reservista TEXT,
                exame_medico TEXT,
                titulo_eleitor TEXT,
                titulo_zona TEXT,
                titulo_secao TEXT,
                pis_pasep TEXT,
                habilitacao TEXT,
                habilitacao_categoria TEXT,
                habilitacao_vencimento TEXT,
                logradouro TEXT,
                numero TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                cep TEXT,
                uf_endereco TEXT,
                alteracao_endereco1 TEXT,
                alteracao_endereco2 TEXT,
                alteracao_endereco3 TEXT,
                cor TEXT,
                altura TEXT,
                peso TEXT,
                olhos TEXT,
                cabelos TEXT,
                sinais TEXT,
                data_chegada_brasil TEXT,
                pais_origem TEXT,
                carteira_modelo19 TEXT,
                registro_geral TEXT,
                conjuge_estrangeiro TEXT,
                quantos_filhos INTEGER,
                conjuge_brasileiro TEXT,
                filhos_brasileiros TEXT,
                raca_cor TEXT,
                foto_path TEXT
            )
        ''')
        self.conn.commit()

    def criar_interface(self):
        # Frame do destaque
        frame_destaque = tk.Frame(self, bg='#00008B')
        frame_destaque.grid(row=0, column=0, sticky='ew')
        self.grid_columnconfigure(0, weight=1)

        label_principal = tk.Label(frame_destaque, text='CADASTRAR FUNCIONÁRIO',
                                   fg="#FFFFFF", bg="#00008B", font=("Arial", 14, "bold"))
        label_principal.pack(anchor='center')

        # Criar notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        
        # Criar abas
        self.aba_dados = ttk.Frame(self.notebook)
        self.aba_documentos = ttk.Frame(self.notebook)
        self.aba_endereco = ttk.Frame(self.notebook)
        self.aba_caracteristicas = ttk.Frame(self.notebook)
        self.aba_estrangeiro = ttk.Frame(self.notebook)
        self.aba_dependentes = ttk.Frame(self.notebook)
        self.aba_codigo_ponto = ttk.Frame(self.notebook)
        self.aba_config_horarios = ttk.Frame(self.notebook)
        
        self.notebook.add(self.aba_dados, text='Dados Pessoais')
        self.notebook.add(self.aba_documentos, text='Documentos')
        self.notebook.add(self.aba_endereco, text='Endereço')
        self.notebook.add(self.aba_caracteristicas, text='Características')
        self.notebook.add(self.aba_estrangeiro, text='Estrangeiro')
        self.notebook.add(self.aba_dependentes, text='Dependentes')
        self.notebook.add(self.aba_codigo_ponto, text="Codigo ponto")
        self.notebook.add(self.aba_config_horarios, text="Config Horarios")
        
        
        #self.notebook.add(self.abas["codigo_ponto"], text="Código de Ponto")
        #self.notebook.add(self.abas["config_horarios"], text="Configurar Horários")
        
        # Criar conteúdo das abas
        self.criar_aba_dados()
        self.criar_aba_documentos()
        self.criar_aba_endereco()
        self.criar_aba_caracteristicas()
        self.criar_aba_estrangeiro()
        self.criar_aba_dependentes()
        
        self.criar_aba_codigo_ponto()
        self.criar_aba_config_horarios()
        
        # Frame de botões
        frame_botoes = tk.Frame(self, bg='#FFFFFF')
        frame_botoes.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        
        botao_salvar = tk.Button(frame_botoes, text='SALVAR', font=('Arial', 12, 'bold'),
                                 bg='#00008B', fg='#FFFFFF', width=12, command=self.salvar_dados)
        botao_salvar.pack(side='left', padx=5)

        botao_novo = tk.Button(frame_botoes, text='NOVO CADASTRO', font=('Arial', 12, 'bold'),
                               bg='#00008B', fg='#FFFFFF', width=15, command=self.limpar_campos)
        botao_novo.pack(side='right', padx=5)

    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho:
            try:
                self.foto_path = caminho
                imagem = Image.open(caminho).convert("RGB")
                imagem = imagem.resize((120, 150))
                imagem_tk = ImageTk.PhotoImage(imagem)

                self.label_foto.config(image=imagem_tk, text="")
                self.label_foto.image = imagem_tk
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao carregar imagem:\n{e}")
                
                
    #------------------------------------------------------
    
    def carregar_dados(self):
        try:
            if os.path.exists("funcionarios.json"):
                with open("funcionarios.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def carregar_horarios(self):
        try:
            if os.path.exists("horarios.json"):
                with open("horarios.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def carregar_registros(self):
        try:
            if os.path.exists("registros_ponto.json"):
                with open("registros_ponto.json", "r") as f:
                    return json.load(f)
        except:
            pass
        return {}

    def salvar_dados(self):
        with open("funcionarios.json", "w") as f:
            json.dump(self.dados_funcionarios, f, indent=2)

    def salvar_horarios(self):
        with open("horarios.json", "w") as f:
            json.dump(self.horarios_config, f, indent=2)

    def salvar_registros(self):
        with open("registros_ponto.json", "w") as f:
            json.dump(self.registros_ponto, f, indent=2)

    def salvar_tudo(self):
        self.salvar_dados()
        self.salvar_horarios()
        self.salvar_registros()
        messagebox.showinfo("Sucesso", "Todos os dados foram salvos com sucesso!")

    def limpar_tudo(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todos os dados?"):
            self.dados_funcionarios = {}
            self.horarios_config = {}
            self.registros_ponto = {}
            self.salvar_tudo()
            messagebox.showinfo("Sucesso", "Todos os dados foram limpos!")

    def sair(self):
        self.salvar_tudo()
        self.master.destroy()

    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho:
            imagem = Image.open(caminho)
            imagem = imagem.resize((120, 150))
            imagem_tk = ImageTk.PhotoImage(imagem)
            self.label_foto.config(image=imagem_tk)
            self.label_foto.image = imagem_tk
            self.foto_path = caminho    
    
    #-----------------------------------------------------
    def criar_aba_dados(self):
        frame = self.aba_dados
        
        # Frame da foto
        foto_frame = tk.LabelFrame(frame, text="Foto", bg='#FFFFFF')
        foto_frame.grid(row=0, column=0, rowspan=10, padx=10, pady=10, sticky='ns')
        
        self.label_foto = tk.Label(foto_frame, text="Sem Foto", bg="white")
        self.label_foto.pack(pady=10)

        btn_foto = tk.Button(foto_frame, text="Selecionar Foto", command=self.selecionar_foto)
        btn_foto.pack(pady=5, padx=10,fill='x')

        # Frame de dados
        dados_frame = tk.LabelFrame(frame, text="Informações Pessoais", bg='#FFFFFF')
        dados_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        # Campos originais + novos
        campos = [
            ('Nome:', 0, 0), ('Matrícula:', 1, 0), ('Contato:', 2, 0),
            ('Idade:', 3, 0), ('Data de nascimento:', 4, 0), ('CPF:', 5, 0),
            ('RG:', 6, 0), ('Cargo:', 7, 0), ('Salário:', 8, 0),
            ('Data de admissão:', 9, 0),
            ('Filiação - Mãe:', 10, 0), ('Filiação - Pai:', 11, 0),
            ('Local Nascimento:', 12, 0), ('Nacionalidade:', 13, 0),
            ('UF Nascimento:', 14, 0), ('Estado Civil:', 15, 0),
            ('Cônjuge:', 16, 0), ('Certidão Casamento:', 17, 0)
        ]
        
        self.campos = {}
        for texto, linha, coluna in campos:
            label = tk.Label(dados_frame, text=texto, fg='#000000', bg='#FFFFFF', font=('Arial', 10))
            label.grid(row=linha, column=coluna, sticky='w', padx=5, pady=2)
            
            entry = tk.Entry(dados_frame, width=30, font=('Arial', 10), relief='solid')
            entry.grid(row=linha, column=coluna+1, sticky='we', padx=5, pady=2)
            
            chave = texto.strip(':').lower().replace(' ', '_').replace('-', '').replace('ç', 'c').replace('ã', 'a')
            self.campos[chave] = entry

        # Contratação
        label_contratacao = tk.Label(dados_frame, text='Contratação:', fg='#000000', bg='#FFFFFF', font=('Arial', 10))
        label_contratacao.grid(row=18, column=0, sticky='w', padx=5, pady=2)
        self.combo_contratacao = ttk.Combobox(dados_frame, values=['Fixa', 'Horista'], width=10, font=('Arial', 10))
        self.combo_contratacao.grid(row=18, column=1, sticky='w', padx=5, pady=2)

        # Ativo
        label_ativo = tk.Label(dados_frame, text='Funcionário Ativo:', fg='#000000', bg='#FFFFFF', font=('Arial', 10))
        label_ativo.grid(row=19, column=0, sticky='w', padx=5, pady=2)
        self.combo_ativo = ttk.Combobox(dados_frame, values=['Sim', 'Não'], width=10, font=('Arial', 10))
        self.combo_ativo.grid(row=19, column=1, sticky='w', padx=5, pady=2)

        # Configurar pesos
        dados_frame.columnconfigure(1, weight=1)
        frame.columnconfigure(1, weight=1)

    def criar_aba_documentos(self):
        frame = self.aba_documentos
        frame.columnconfigure(1, weight=1)
        
        campos = [
            ("RG Emissão:", 0, 0), ("Órgão Emissor:", 0, 2), ("RG Data:", 0, 4),
            ("CPF:", 1, 0), ("Cart. Profissional:", 1, 2), ("Conselho:", 1, 4),
            ("CTPS:", 2, 0), ("Série:", 2, 2), ("Cart. Reservista:", 2, 4), ("Exame Médico:", 2, 6),
            ("Título Eleitor:", 3, 0), ("Zona:", 3, 2), ("Seção:", 3, 4), ("PIS/PASEP:", 3, 6),
            ("Habilitação:", 4, 0), ("Categoria:", 4, 2), ("Vencimento:", 4, 4)
        ]
        
        self.campos_documentos = {}
        for texto, linha, coluna in campos:
            lbl = tk.Label(frame, text=texto, fg='#000000', bg='#FFFFFF', font=('Arial', 10))
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            entry = tk.Entry(frame, font=('Arial', 10))
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='we')
            
            chave = texto.strip(':').lower().replace(' ', '_').replace('.', '').replace('ç', 'c')
            self.campos_documentos[chave] = entry

    def criar_aba_endereco(self):
        frame = self.aba_endereco
        
        campos = [
            ("Logradouro:", 0, 0), ("Nº:", 0, 2), ("Complemento:", 1, 0),
            ("Bairro:", 2, 0), ("Cidade:", 3, 0), ("CEP:", 3, 2),
            ("UF:", 3, 4), ("Alteração Endereço 1:", 4, 0),
            ("Alteração Endereço 2:", 5, 0), ("Alteração Endereço 3:", 6, 0)
        ]
        
        self.campos_endereco = {}
        for texto, linha, coluna in campos:
            lbl = tk.Label(frame, text=texto, fg='#000000', bg='#FFFFFF', font=('Arial', 10))
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            if texto == "UF:":
                entry = tk.Entry(frame, width=5, font=('Arial', 10))
            else:
                entry = tk.Entry(frame, font=('Arial', 10))
                
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='we')
            
            chave = texto.strip(':').lower().replace(' ', '_').replace('ç', 'c').replace('ã', 'a')
            self.campos_endereco[chave] = entry

    def criar_aba_caracteristicas(self):
        frame = self.aba_caracteristicas
        
        campos = [
            ("Cor:", 0, 0), ("Altura:", 0, 2), ("Peso:", 0, 4),
            ("Olhos:", 1, 0), ("Cabelos:", 1, 2), ("Sinais:", 1, 4)
        ]
        
        self.campos_caracteristicas = {}
        for texto, linha, coluna in campos:
            lbl = tk.Label(frame, text=texto, fg='#000000', bg='#FFFFFF', font=('Arial', 10))
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=5)
            
            entry = tk.Entry(frame, width=15, font=('Arial', 10))
            entry.grid(row=linha, column=coluna+1, padx=5, pady=5, sticky='w')
            
            chave = texto.strip(':').lower()
            self.campos_caracteristicas[chave] = entry

    def criar_aba_estrangeiro(self):
        frame = self.aba_estrangeiro
        
        campos = [
            ("Data chegada Brasil:", 0, 0), ("País origem:", 0, 2),
            ("Carteira modelo 19:", 1, 0), ("Nº Registro Geral:", 1, 2),
            ("Estado Civil:", 2, 0), ("Cônjuge nome:", 3, 0),
            ("Quantos filhos:", 4, 0)
        ]
        
        self.campos_estrangeiro = {}
        for texto, linha, coluna in campos:
            lbl = tk.Label(frame, text=texto, fg='#000000', bg='#FFFFFF', font=('Arial', 10))
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            entry = tk.Entry(frame, font=('Arial', 10))
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='w')
            
            chave = texto.lower().replace(' ', '_').replace(':', '').replace('ã', 'a')
            self.campos_estrangeiro[chave] = entry

        # Radiobuttons
        lbl_conjuge = tk.Label(frame, text="Cônjuge brasileiro:", fg='#000000', bg='#FFFFFF', font=('Arial', 10))
        lbl_conjuge.grid(row=2, column=2, sticky='e', padx=5, pady=2)
        
        self.conjuge_brasileiro = tk.StringVar()
        rb_sim = tk.Radiobutton(frame, text="Sim", variable=self.conjuge_brasileiro, 
                               value="Sim", bg='#FFFFFF')
        rb_sim.grid(row=2, column=3, sticky='w')
        
        rb_nao = tk.Radiobutton(frame, text="Não", variable=self.conjuge_brasileiro, 
                               value="Não", bg='#FFFFFF')
        rb_nao.grid(row=2, column=4, sticky='w')

        lbl_filhos = tk.Label(frame, text="Filhos brasileiros:", fg='#000000', bg='#FFFFFF', font=('Arial', 10))
        lbl_filhos.grid(row=3, column=0, sticky='e', padx=5, pady=2)
        
        self.filhos_brasileiros = tk.StringVar()
        rb_sim_f = tk.Radiobutton(frame, text="Sim", variable=self.filhos_brasileiros, 
                                 value="Sim", bg='#FFFFFF')
        rb_sim_f.grid(row=3, column=1, sticky='w')
        
        rb_nao_f = tk.Radiobutton(frame, text="Não", variable=self.filhos_brasileiros, 
                                 value="Não", bg='#FFFFFF')
        rb_nao_f.grid(row=3, column=2, sticky='w')

        # Checkbuttons para raça/cor
        raca_frame = tk.LabelFrame(frame, text="Raça/Cor", bg='#FFFFFF')
        raca_frame.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='we')
        
        racas = ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Não declarado"]
        self.raca_vars = {}
        
        for i, raca in enumerate(racas):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(raca_frame, text=raca, variable=var, bg='#FFFFFF')
            cb.grid(row=0, column=i, padx=5, pady=2, sticky='w')
            self.raca_vars[raca] = var

    def criar_aba_dependentes(self):
        frame = self.aba_dependentes
        
        # Cabeçalho
        headers = ["Nome", "Data Nascimento", "Parentesco"]
        for col, header in enumerate(headers):
            lbl = tk.Label(frame, text=header, fg='#000000', bg='#FFFFFF', 
                          font=("Arial", 10, "bold"))
            lbl.grid(row=0, column=col, padx=5, pady=5, sticky='w')
        
        # Linhas para dependentes
        self.dependentes_entries = []
        for i in range(5):
            entries_linha = []
            for col in range(3):
                entry = tk.Entry(frame, font=('Arial', 10))
                entry.grid(row=i+1, column=col, padx=5, pady=2, sticky='we')
                entries_linha.append(entry)
            self.dependentes_entries.append(entries_linha)
        
        # Configurar pesos das colunas
        for col in range(3):
            frame.columnconfigure(col, weight=1)
            
    
    def criar_aba_codigo_ponto(self):
        frame = self.aba_codigo_ponto  # Corrigido para usar self.aba_codigo_ponto diretamente

        # Header
        ttk.Label(frame, text="Gerador de Código de Ponto", style="Header.TLabel").grid(
            row=0, column=0, columnspan=3, pady=10
        )

        # Frame do código
        codigo_frame = ttk.LabelFrame(frame, text="Código de Ponto")
        codigo_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.codigo_var = tk.StringVar(value="Ainda não gerado")

        ttk.Label(codigo_frame, text="Código:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        lbl_codigo = ttk.Label(codigo_frame, textvariable=self.codigo_var, font=("Arial", 14, "bold"), foreground="blue")
        lbl_codigo.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        # Botões
        ttk.Button(frame, text="Gerar Novo Código", command=self.gerar_codigo).grid(row=3, column=0, padx=5, pady=10)
        ttk.Button(frame, text="Copiar Código", command=self.copiar_codigo).grid(row=3, column=1, padx=5, pady=10)
        ttk.Button(frame, text="Salvar Código", command=self.salvar_codigo).grid(row=3, column=2, padx=5, pady=10)

        # Pesos
        frame.columnconfigure(1, weight=1)
        codigo_frame.columnconfigure(1, weight=1)


    def atualizar_combobox_funcionarios(self):
            funcionarios = [f"{mat} - {dados['nome']}" for mat, dados in self.dados_funcionarios.items()]
            self.cb_funcionarios['values'] = funcionarios
            if funcionarios:
                self.cb_funcionarios.current(0)

    def gerar_codigo(self):
            # Gerar código alfanumérico único
            codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            self.codigo_var.set(codigo)
            return codigo

    def copiar_codigo(self):
            self.master.clipboard_clear()
            self.master.clipboard_append(self.codigo_var.get())
            messagebox.showinfo("Copiado", "Código copiado para a área de transferência!")

    def salvar_codigo(self):
            funcionario = self.funcionario_var.get()
            if not funcionario:
                messagebox.showerror("Erro", "Selecione um funcionário!")
                return
                
            matricula = funcionario.split(" - ")[0]
            codigo = self.codigo_var.get()
            
            if matricula in self.dados_funcionarios:
                self.dados_funcionarios[matricula]['codigo_ponto'] = codigo
                messagebox.showinfo("Sucesso", f"Código salvo para {self.dados_funcionarios[matricula]['nome']}!")
            else:
                messagebox.showerror("Erro", "Funcionário não encontrado!")

    def criar_aba_config_horarios(self):
            frame = self.aba_config_horarios
            
            # Header
            ttk.Label(frame, text="Configuração de Horários", style="Header.TLabel").grid(
                row=0, column=0, columnspan=4, pady=10
            )
            
                
            # Horários padrão
            horarios_frame = ttk.LabelFrame(frame, text="Horários Padrão")
            horarios_frame.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
            
            horarios = [
                ("Entrada:", 0, 0),
                ("Saída Almoço:", 0, 2),
                ("Retorno Almoço:", 1, 0),
                ("Saída:", 1, 2),
                ("Café (Manhã):", 2, 0),
                ("Café (Tarde):", 2, 2),
                ("Hora Extra Início:", 3, 0)
            ]
            
            self.entries_horarios = {}
            for texto, linha, coluna in horarios:
                ttk.Label(horarios_frame, text=texto).grid(row=linha, column=coluna, padx=5, pady=5, sticky='e')
                entry = ttk.Entry(horarios_frame, width=8)
                entry.grid(row=linha, column=coluna+1, padx=5, pady=5, sticky='w')
                self.entries_horarios[texto.replace(':', '').lower().replace(' ', '_')] = entry
            
            # Dias da semana
            dias_frame = ttk.LabelFrame(frame, text="Dias de Trabalho")
            dias_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
            
            dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
            self.dias_vars = {}
            
            for i, dia in enumerate(dias_semana):
                var = tk.BooleanVar(value=True if i < 5 else False)
                cb = ttk.Checkbutton(dias_frame, text=dia, variable=var)
                cb.grid(row=0, column=i, padx=5, pady=5)
                self.dias_vars[dia.lower()] = var
            
            # Botões
            btn_salvar = ttk.Button(frame, text="Salvar Configuração", command=self.salvar_config_horarios)
            btn_salvar.grid(row=4, column=1, pady=10, padx=5)
            
            btn_carregar = ttk.Button(frame, text="Carregar Configuração", command=self.carregar_config_horarios)
            btn_carregar.grid(row=4, column=2, pady=10, padx=5)
            
     
            # Configurar pesos
            frame.columnconfigure(1, weight=1)
            horarios_frame.columnconfigure(1, weight=1)
            horarios_frame.columnconfigure(3, weight=1)

    def salvar_config_horarios(self):
            funcionario = self.func_horario_var.get()
            if not funcionario:
                messagebox.showerror("Erro", "Selecione um funcionário!")
                return
                
            matricula = funcionario.split(" - ")[0]
            
            config = {}
            for chave, entry in self.entries_horarios.items():
                config[chave] = entry.get()
            
            # Dias de trabalho
            dias_trabalho = []
            for dia, var in self.dias_vars.items():
                if var.get():
                    dias_trabalho.append(dia)
            config['dias_trabalho'] = dias_trabalho
            
            self.horarios_config[matricula] = config
            messagebox.showinfo("Sucesso", "Configuração de horários salva com sucesso!")

    def carregar_config_horarios(self):
            funcionario = self.func_horario_var.get()
            if not funcionario:
                messagebox.showerror("Erro", "Selecione um funcionário!")
                return
                
            matricula = funcionario.split(" - ")[0]
            
            if matricula in self.horarios_config:
                config = self.horarios_config[matricula]
                
                # Preencher campos
                for chave, entry in self.entries_horarios.items():
                    if chave in config:
                        entry.delete(0, tk.END)
                        entry.insert(0, config[chave])
                
                # Preencher dias de trabalho
                dias_trabalho = config.get('dias_trabalho', [])
                for dia, var in self.dias_vars.items():
                    var.set(dia in dias_trabalho)
            else:
                messagebox.showinfo("Info", "Nenhuma configuração encontrada para este funcionário")

        
              
    #---------------------------------------------------   
            
            
            

    def salvar_dados(self):
        confirmar = messagebox.askyesno("Confirmação", "Deseja salvar os dados?")
        if not confirmar:
            messagebox.showwarning("Cancelado", "O salvamento foi cancelado.")
            return

        try:
            # Coletar dados das abas
            dados = {
                'nome': self.campos['nome'].get(),
                'matricula': self.campos['matrícula'].get(),
                'contato': self.campos['contato'].get(),
                'idade': self.campos['idade'].get(),
                'data_nascimento': self.campos['data_de_nascimento'].get(),
                'cpf': self.campos['cpf'].get(),
                'rg': self.campos['rg'].get(),
                'tipo_contratacao': self.combo_contratacao.get(),
                'cargo': self.campos['cargo'].get(),
                'salario': self.campos['salário'].get(),
                'data_admissao': self.campos['data_de_admissão'].get(),
                'ativo': self.combo_ativo.get(),
                'foto_path': getattr(self, 'foto_path', ''),
                
                # Dados adicionais
                'filiacao_mae': self.campos['filiação_mae'].get(),
                'filiacao_pai': self.campos['filiação_pai'].get(),
                'local_nascimento': self.campos['local_nascimento'].get(),
                'nacionalidade': self.campos['nacionalidade'].get(),
                'uf_nascimento': self.campos['uf_nascimento'].get(),
                'estado_civil': self.campos['estado_civil'].get(),
                'conjuge': self.campos['cônjuge'].get(),
                'certidao_casamento': self.campos['certidão_casamento'].get(),
                
                # Documentos
                'rg_emissao': self.campos_documentos['rg_emissão'].get(),
                'rg_orgao_emissor': self.campos_documentos['rg_orgao_emissor'].get(),
                'rg_data_emissao': self.campos_documentos['rg_data'].get(),
                'cart_profissional': self.campos_documentos['cart_profissional'].get(),
                'conselho': self.campos_documentos['conselho'].get(),
                'ctps': self.campos_documentos['ctps'].get(),
                'ctps_serie': self.campos_documentos['série'].get(),
                'cart_reservista': self.campos_documentos['cart_reservista'].get(),
                'exame_medico': self.campos_documentos['exame_médico'].get(),
                'titulo_eleitor': self.campos_documentos['título_eleitor'].get(),
                'titulo_zona': self.campos_documentos['zona'].get(),
                'titulo_secao': self.campos_documentos['seção'].get(),
                'pis_pasep': self.campos_documentos['pispasep'].get(),
                'habilitacao': self.campos_documentos['habilitação'].get(),
                'habilitacao_categoria': self.campos_documentos['categoria'].get(),
                'habilitacao_vencimento': self.campos_documentos['vencimento'].get(),
                
                # Endereço
                'logradouro': self.campos_endereco['logradouro'].get(),
                'numero': self.campos_endereco['nº'].get(),
                'complemento': self.campos_endereco['complemento'].get(),
                'bairro': self.campos_endereco['bairro'].get(),
                'cidade': self.campos_endereco['cidade'].get(),
                'cep': self.campos_endereco['cep'].get(),
                'uf_endereco': self.campos_endereco['uf'].get(),
                'alteracao_endereco1': self.campos_endereco['alteração_endereço_1'].get(),
                'alteracao_endereco2': self.campos_endereco['alteração_endereço_2'].get(),
                'alteracao_endereco3': self.campos_endereco['alteração_endereço_3'].get(),
                
                # Características
                'cor': self.campos_caracteristicas['cor'].get(),
                'altura': self.campos_caracteristicas['altura'].get(),
                'peso': self.campos_caracteristicas['peso'].get(),
                'olhos': self.campos_caracteristicas['olhos'].get(),
                'cabelos': self.campos_caracteristicas['cabelos'].get(),
                'sinais': self.campos_caracteristicas['sinais'].get(),
                
                # Estrangeiro
                'data_chegada_brasil': self.campos_estrangeiro['data_chegada_brasil'].get(),
                'pais_origem': self.campos_estrangeiro['país_origem'].get(),
                'carteira_modelo19': self.campos_estrangeiro['carteira_modelo_19'].get(),
                'registro_geral': self.campos_estrangeiro['nº_registro_geral'].get(),
                'conjuge_estrangeiro': self.campos_estrangeiro['cônjuge_nome'].get(),
                'quantos_filhos': self.campos_estrangeiro['quantos_filhos'].get(),
                'conjuge_brasileiro': self.conjuge_brasileiro.get(),
                'filhos_brasileiros': self.filhos_brasileiros.get(),
                
                # Raça/Cor
                'raca_cor': ', '.join([r for r, var in self.raca_vars.items() if var.get()]),
                
                # Dependentes
                'dependentes': ';'.join(
                    [','.join([entry.get() for entry in linha]) 
                     for linha in self.dependentes_entries]
                )
            }

            # Montar a query SQL
            colunas = ', '.join(dados.keys())
            placeholders = ', '.join(['?'] * len(dados))
            
            self.cursor.execute(f'''
                INSERT INTO funcionarios ({colunas})
                VALUES ({placeholders})
            ''', tuple(dados.values()))
            
            self.conn.commit()
            messagebox.showinfo("Salvo", "Dados salvos com sucesso!")
            self.limpar_campos()

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

    def limpar_campos(self):
        # Limpar campos principais
        for campo in self.campos.values():
            campo.delete(0, tk.END)
        
        # Limpar comboboxes
        self.combo_contratacao.set('')
        self.combo_ativo.set('')
        
        # Limpar campos das outras abas
        for campo in self.campos_documentos.values():
            campo.delete(0, tk.END)
            
        for campo in self.campos_endereco.values():
            campo.delete(0, tk.END)
            
        for campo in self.campos_caracteristicas.values():
            campo.delete(0, tk.END)
            
        for campo in self.campos_estrangeiro.values():
            campo.delete(0, tk.END)
            
        for linha in self.dependentes_entries:
            for campo in linha:
                campo.delete(0, tk.END)
                
        # Limpar radio buttons
        self.conjuge_brasileiro.set('')
        self.filhos_brasileiros.set('')
        
        # Limpar checkboxes
        for var in self.raca_vars.values():
            var.set(False)
            
        # Limpar foto
        self.label_foto.config(image='', text="Sem Foto")
        self.foto_path = ''


if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroFuncionario(root)
    root.mainloop()
