import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

class FichaFuncionalApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ficha Funcional")
        self.master.geometry("900x600")
        self.master.resizable(True, True)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TNotebook", background="#e0e0e0")
        self.style.configure("TNotebook.Tab", font=("Arial", 10, "bold"), padding=(10, 5))
        
        # Criar notebook
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Criar abas
        self.abas = {
            "dados_pessoais": ttk.Frame(self.notebook),
            "documentos": ttk.Frame(self.notebook),
            "endereco": ttk.Frame(self.notebook),
            "caracteristicas": ttk.Frame(self.notebook),
            "estrangeiro": ttk.Frame(self.notebook),
            "dependentes": ttk.Frame(self.notebook)
        }
        
        # Adicionar abas ao notebook
        for nome, frame in self.abas.items():
            self.notebook.add(frame, text=nome.replace('_', ' ').title())
        
        # Criar conteúdo das abas
        self.criar_aba_dados_pessoais()
        self.criar_aba_documentos()
        self.criar_aba_endereco()
        self.criar_aba_caracteristicas()
        self.criar_aba_estrangeiro()
        self.criar_aba_dependentes()
        
        # Botão de salvar
        btn_salvar = ttk.Button(self.master, text="Salvar Ficha", command=self.salvar_ficha)
        btn_salvar.pack(pady=10)


    def selecionar_foto(self):
        caminho = filedialog.askopenfilename(filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho:
            try:
                imagem = Image.open(caminho).convert("RGB")
                imagem = imagem.resize((120, 150))
                imagem_tk = ImageTk.PhotoImage(imagem)

                self.label_foto.config(image=imagem_tk, text="")
                self.label_foto.image = imagem_tk  # Mantém referência
                
            except Exception as e:
                tk.messagebox.showerror("Erro", f"Falha ao carregar imagem:\n{e}")



    def criar_aba_dados_pessoais(self):
        frame = self.abas["dados_pessoais"]
        
        # Frame da foto
        foto_frame = ttk.LabelFrame(frame, text="Foto")
        foto_frame.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky='ns')
        
        self.label_foto = tk.Label(foto_frame, text="Sem Foto", bg="white")
        self.label_foto.pack(pady=10)

        
        btn_foto = tk.Button(foto_frame, text="Selecionar Foto", command=self.selecionar_foto)
        btn_foto.pack(pady=5, padx=10, fill='x')

        # Frame de dados
        dados_frame = ttk.LabelFrame(frame, text="Informações Pessoais")
        dados_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        
        campos = [
            ("Matrícula:", 0, 0),
            ("Nome:", 1, 0),
            ("Filiação - Mãe:", 2, 0),
            ("Filiação - Pai:", 3, 0),
            ("Data Nascimento:", 4, 0),
            ("Local Nascimento:", 5, 0),
            ("Nacionalidade:", 6, 0),
            ("UF:", 6, 2),
            ("Estado Civil:", 7, 0),
            ("Cônjuge:", 8, 0),
            ("Certidão Casamento:", 9, 0)
        ]
        
        self.entries_dados = {}
        for texto, linha, coluna in campos:
            lbl = ttk.Label(dados_frame, text=texto)
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            if texto == "UF:":
                entry = ttk.Entry(dados_frame, width=5)
                entry.grid(row=linha, column=coluna+1, sticky='w', padx=5, pady=2)
            else:
                entry = ttk.Entry(dados_frame, width=30)
                span = 1 if texto == "UF:" else (3 if coluna == 0 else 1)
                entry.grid(row=linha, column=coluna+1, columnspan=span, sticky='we', padx=5, pady=2)
                
            chave = texto.lower().replace(' ', '_').replace(':', '').replace('ç', 'c').replace('ã', 'a')
            self.entries_dados[chave] = entry

        # Configurar pesos da grid
        frame.columnconfigure(1, weight=1)
        dados_frame.columnconfigure(1, weight=1)

    def criar_aba_documentos(self):
        frame = self.abas["documentos"]
        frame.columnconfigure(1, weight=1)
        
        campos = [
            ("RG:", 0, 0, 1),
            ("Emissão:", 0, 2, 1),
            ("Órgão Emissor:", 0, 4, 1),
            ("Data:", 0, 6, 1),
            ("CPF:", 1, 0, 1),
            ("Cart. Profissional:", 1, 2, 1),
            ("Conselho:", 1, 4, 1),
            ("CTPS:", 2, 0, 1),
            ("Série:", 2, 2, 1),
            ("Cart. Reservista:", 2, 4, 1),
            ("Exame Médico:", 2, 6, 1),
            ("Título Eleitor:", 3, 0, 1),
            ("Zona:", 3, 2, 1),
            ("Seção:", 3, 4, 1),
            ("PIS/PASEP:", 3, 6, 1),
            ("Habilitação:", 4, 0, 1),
            ("Categoria:", 4, 2, 1),
            ("Vencimento:", 4, 4, 1)
        ]
        
        self.entries_documentos = {}
        for texto, linha, coluna, span in campos:
            lbl = ttk.Label(frame, text=texto)
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            entry = ttk.Entry(frame)
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='we', columnspan=span)
            
            chave = texto.strip(':').lower().replace(' ', '_').replace('.', '')
            self.entries_documentos[chave] = entry

    def criar_aba_endereco(self):
        frame = self.abas["endereco"]
        
        campos = [
            ("Logradouro:", 0, 0, 4),
            ("Nº:", 0, 5, 1),
            ("Complemento:", 1, 0, 6),
            ("Bairro:", 2, 0, 6),
            ("Cidade:", 3, 0, 1),
            ("CEP:", 3, 2, 1),
            ("UF:", 3, 4, 1),
            ("Alteração Endereço 1:", 4, 0, 6),
            ("Alteração Endereço 2:", 5, 0, 6),
            ("Alteração Endereço 3:", 6, 0, 6)
        ]
        
        self.entries_endereco = {}
        for texto, linha, coluna, span in campos:
            lbl = ttk.Label(frame, text=texto)
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            if texto == "UF:":
                entry = ttk.Entry(frame, width=5)
            else:
                entry = ttk.Entry(frame)
                
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='we', columnspan=span)
            
            chave = texto.lower().replace(' ', '_').replace(':', '').replace('ç', 'c').replace('ã', 'a')
            self.entries_endereco[chave] = entry

        # Configurar pesos
        for col in [1, 3, 5]:
            frame.columnconfigure(col, weight=1)

    def criar_aba_caracteristicas(self):
        frame = self.abas["caracteristicas"]
        
        campos = [
            ("Cor:", 0, 0),
            ("Altura:", 0, 2),
            ("Peso:", 0, 4),
            ("Olhos:", 1, 0),
            ("Cabelos:", 1, 2),
            ("Sinais:", 1, 4)
        ]
        
        self.entries_caracteristicas = {}
        for texto, linha, coluna in campos:
            lbl = ttk.Label(frame, text=texto)
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=5)
            
            entry = ttk.Entry(frame, width=15)
            entry.grid(row=linha, column=coluna+1, padx=5, pady=5, sticky='w')
            
            chave = texto.strip(':').lower()
            self.entries_caracteristicas[chave] = entry

    def criar_aba_estrangeiro(self):
        frame = self.abas["estrangeiro"]
        
        # Parte superior
        campos_superior = [
            ("Data chegada Brasil:", 0, 0),
            ("País origem:", 0, 2),
            ("Carteira modelo 19:", 1, 0),
            ("Nº Registro Geral:", 1, 2),
            ("Estado Civil:", 2, 0),
            ("Cônjuge nome:", 3, 2),
            ("Quantos filhos:", 4, 0)
        ]
        
        self.entries_estrangeiro = {}
        for texto, linha, coluna in campos_superior:
            lbl = ttk.Label(frame, text=texto)
            lbl.grid(row=linha, column=coluna, sticky='e', padx=5, pady=2)
            
            entry = ttk.Entry(frame)
            entry.grid(row=linha, column=coluna+1, padx=5, pady=2, sticky='w')
            
            chave = texto.lower().replace(' ', '_').replace(':', '').replace('ã', 'a')
            self.entries_estrangeiro[chave] = entry

        # Radiobuttons
        ttk.Label(frame, text="Cônjuge brasileiro:").grid(row=2, column=2, sticky='e', padx=5, pady=2)
        self.conjuge_brasileiro = tk.StringVar()
        ttk.Radiobutton(frame, text="Sim", variable=self.conjuge_brasileiro, value="sim").grid(row=2, column=3, sticky='w')
        ttk.Radiobutton(frame, text="Não", variable=self.conjuge_brasileiro, value="nao").grid(row=2, column=4, sticky='w')
        
        ttk.Label(frame, text="Filhos brasileiros:").grid(row=3, column=0, sticky='e', padx=5, pady=2)
        self.filhos_brasileiros = tk.StringVar()
        ttk.Radiobutton(frame, text="Sim", variable=self.filhos_brasileiros, value="sim").grid(row=3, column=1, sticky='w')
        ttk.Radiobutton(frame, text="Não", variable=self.filhos_brasileiros, value="nao").grid(row=3, column=2, sticky='w')

        # Checkbuttons para raça/cor
        raca_frame = ttk.LabelFrame(frame, text="Raça/Cor")
        raca_frame.grid(row=5, column=0, columnspan=5, padx=10, pady=10, sticky='we')
        
        racas = ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Não declarado"]
        self.raca_vars = []
        
        for i, raca in enumerate(racas):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(raca_frame, text=raca, variable=var)
            cb.grid(row=0, column=i, padx=5, pady=2, sticky='w')
            self.raca_vars.append((raca, var))

    def criar_aba_dependentes(self):
        frame = self.abas["dependentes"]
        
        # Cabeçalho
        headers = ["Nome", "Data Nascimento", "Parentesco"]
        for col, header in enumerate(headers):
            ttk.Label(frame, text=header, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5, sticky='w')
        
        # Linhas para dependentes
        self.dependentes_entries = []
        for i in range(5):
            entries_linha = []
            for col in range(3):
                entry = ttk.Entry(frame)
                entry.grid(row=i+1, column=col, padx=5, pady=2, sticky='we')
                entries_linha.append(entry)
            self.dependentes_entries.append(entries_linha)
        
        # Configurar pesos das colunas
        for col in range(3):
            frame.columnconfigure(col, weight=1)

    def salvar_ficha(self):
        # Implemente aqui a lógica para salvar os dados
        print("Ficha salva com sucesso!")
        tk.messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    app = FichaFuncionalApp(root)
    root.mainloop()