
    def criar_aba_relatorios(self):
        frame = self.abas["relatorios"]
        
        # Header
        ttk.Label(frame, text="Relatórios e Controle", style="Header.TLabel").grid(
            row=0, column=0, columnspan=3, pady=10
        )
        
        # Seleção de funcionário
        ttk.Label(frame, text="Funcionário:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.func_relatorio_var = tk.StringVar()
        cb_func_relatorios = ttk.Combobox(frame, textvariable=self.func_relatorio_var, width=40)
        cb_func_relatorios.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        cb_func_relatorios['values'] = [f"{mat} - {dados['nome']}" for mat, dados in self.dados_funcionarios.items()]
        if cb_func_relatorios['values']:
            cb_func_relatorios.current(0)
        
        # Período
        ttk.Label(frame, text="Período:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        
        periodo_frame = ttk.Frame(frame)
        periodo_frame.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        self.data_inicio_var = tk.StringVar()
        self.data_fim_var = tk.StringVar()
        
        ttk.Label(periodo_frame, text="De:").grid(row=0, column=0, padx=2)
        entry_inicio = ttk.Entry(periodo_frame, textvariable=self.data_inicio_var, width=10)
        entry_inicio.grid(row=0, column=1, padx=2)
        ttk.Label(periodo_frame, text="Até:").grid(row=0, column=2, padx=2)
        entry_fim = ttk.Entry(periodo_frame, textvariable=self.data_fim_var, width=10)
        entry_fim.grid(row=0, column=3, padx=2)
        
        # Botões de relatório
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="Relatório Diário", command=self.gerar_relatorio_diario).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Relatório Mensal", command=self.gerar_relatorio_mensal).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Horas Extras", command=self.calcular_horas_extras).pack(side='left', padx=5)
        
        # Área de resultados
        resultado_frame = ttk.LabelFrame(frame, text="Resultado")
        resultado_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        self.text_resultado = tk.Text(resultado_frame, wrap="word", height=15)
        scrollbar = ttk.Scrollbar(resultado_frame, command=self.text_resultado.yview)
        self.text_resultado.config(yscrollcommand=scrollbar.set)
        
        self.text_resultado.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        resultado_frame.columnconfigure(0, weight=1)
        resultado_frame.rowconfigure(0, weight=1)
        
        # Configurar pesos
        frame.columnconfigure(1, weight=1)
        resultado_frame.columnconfigure(0, weight=1)
        resultado_frame.rowconfigure(0, weight=1)

    def gerar_relatorio_diario(self):
        self.text_resultado.delete(1.0, tk.END)
        
        funcionario = self.func_relatorio_var.get()
        if not funcionario:
            messagebox.showerror("Erro", "Selecione um funcionário!")
            return
            
        matricula = funcionario.split(" - ")[0]
        data = self.data_inicio_var.get() or datetime.datetime.now().strftime("%d/%m/%Y")
        
        registros = self.registros_ponto.get(matricula, [])
        registros_dia = [r for r in registros if r['data'] == data]
        
        if not registros_dia:
            self.text_resultado.insert(tk.END, f"Nenhum registro encontrado para {data}")
            return
        
        self.text_resultado.insert(tk.END, f"Relatório Diário - {data}\n")
        self.text_resultado.insert(tk.END, f"Funcionário: {self.dados_funcionarios[matricula]['nome']}\n")
        self.text_resultado.insert(tk.END, "-" * 50 + "\n")
        
        for registro in registros_dia:
            self.text_resultado.insert(tk.END, f"{registro['tipo']}: {registro['hora']}\n")
        
        self.text_resultado.insert(tk.END, "-" * 50 + "\n")
        
        # Calcular horas trabalhadas
        if len(registros_dia) >= 4:
            entrada = datetime.datetime.strptime(registros_dia[0]['hora'], "%H:%M:%S")
            saida_almoco = datetime.datetime.strptime(registros_dia[1]['hora'], "%H:%M:%S")
            retorno_almoco = datetime.datetime.strptime(registros_dia[2]['hora'], "%H:%M:%S")
            saida = datetime.datetime.strptime(registros_dia[3]['hora'], "%H:%M:%S")
            
            manha = saida_almoco - entrada
            tarde = saida - retorno_almoco
            total = manha + tarde
            
            self.text_resultado.insert(tk.END, f"\nTotal de horas trabalhadas: {total}\n")

    def gerar_relatorio_mensal(self):
        self.text_resultado.delete(1.0, tk.END)
        
        funcionario = self.func_relatorio_var.get()
        if not funcionario:
            messagebox.showerror("Erro", "Selecione um funcionário!")
            return
            
        matricula = funcionario.split(" - ")[0]
        mes = datetime.datetime.now().month
        ano = datetime.datetime.now().year
        
        registros = self.registros_ponto.get(matricula, [])
        registros_mes = [r for r in registros 
                        if datetime.datetime.strptime(r['data'], "%d/%m/%Y").month == mes
                        and datetime.datetime.strptime(r['data'], "%d/%m/%Y").year == ano]
        
        if not registros_mes:
            self.text_resultado.insert(tk.END, f"Nenhum registro encontrado para o mês atual")
            return
        
        dias_trabalhados = {}
        for r in registros_mes:
            if r['data'] not in dias_trabalhados:
                dias_trabalhados[r['data']] = []
            dias_trabalhados[r['data']].append(r)
        
        self.text_resultado.insert(tk.END, f"Relatório Mensal - {mes}/{ano}\n")
        self.text_resultado.insert(tk.END, f"Funcionário: {self.dados_funcionarios[matricula]['nome']}\n")
        self.text_resultado.insert(tk.END, "-" * 50 + "\n")
        
        for data, registros in dias_trabalhados.items():
            self.text_resultado.insert(tk.END, f"\n{data}:\n")
            for r in registros:
                self.text_resultado.insert(tk.END, f"  {r['tipo']}: {r['hora']}\n")

    def calcular_horas_extras(self):
        self.text_resultado.delete(1.0, tk.END)
        
        funcionario = self.func_relatorio_var.get()
        if not funcionario:
            messagebox.showerror("Erro", "Selecione um funcionário!")
            return
            
        matricula = funcionario.split(" - ")[0]
        
        # Obter configuração de horário
        horario = self.horarios_config.get(matricula, {})
        if not horario:
            self.text_resultado.insert(tk.END, "Configuração de horário não encontrada!")
            return
        
        # Calcular horas extras para cada dia
        horas_extras = 0
        registros = self.registros_ponto.get(matricula, [])
        
        # Agrupar por dia
        registros_por_dia = {}
        for r in registros:
            if r['data'] not in registros_por_dia:
                registros_por_dia[r['data']] = []
            registros_por_dia[r['data']].append(r)
        
        for data, registros_dia in registros_por_dia.items():
            if len(registros_dia) >= 4:
                entrada = datetime.datetime.strptime(registros_dia[0]['hora'], "%H:%M:%S")
                saida_almoco = datetime.datetime.strptime(registros_dia[1]['hora'], "%H:%M:%S")
                retorno_almoco = datetime.datetime.strptime(registros_dia[2]['hora'], "%H:%M:%S")
                saida = datetime.datetime.strptime(registros_dia[3]['hora'], "%H:%M:%S")
                
                # Calcular horas trabalhadas
                manha = (saida_almoco - entrada).seconds / 3600
                tarde = (saida - retorno_almoco).seconds / 3600
                total_trabalhado = manha + tarde
                
                # Horário padrão (considerando 8 horas)
                horas_padrao = 8.0
                
                # Calcular horas extras
                if total_trabalhado > horas_padrao:
                    extra = total_trabalhado - horas_padrao
                    horas_extras += extra
                    self.text_resultado.insert(tk.END, 
                        f"{data}: +{extra:.2f}h extra (Total: {total_trabalhado:.2f}h)\n")
        
        self.text_resultado.insert(tk.END, f"\nTotal de horas extras: {horas_extras:.2f}h\n")
        self.text_resultado.insert(tk.END, f"Valor estimado: R${horas_extras * 20:.2f} (considerando R$20/h extra)\n")



    def criar_aba_registrar_ponto(self):
        frame = self.abas["registrar_ponto"]
        
        # Header
        ttk.Label(frame, text="Registro de Ponto", style="Header.TLabel").grid(
            row=0, column=0, columnspan=3, pady=10
        )
        
        # Entrada do código
        ttk.Label(frame, text="Código do Funcionário:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        
        self.codigo_registro_var = tk.StringVar()
        entry_codigo = ttk.Entry(frame, textvariable=self.codigo_registro_var, width=20)
        entry_codigo.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        entry_codigo.bind("<Return>", lambda e: self.registrar_ponto())
        
        btn_registrar = ttk.Button(frame, text="Registrar Ponto", command=self.registrar_ponto)
        btn_registrar.grid(row=1, column=2, padx=5, pady=5)
        
        # Informações do funcionário
        self.info_frame = ttk.LabelFrame(frame, text="Informações")
        self.info_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        self.lbl_nome = ttk.Label(self.info_frame, text="Nome: ")
        self.lbl_nome.grid(row=0, column=0, padx=5, pady=2, sticky='w')
        
        self.lbl_cargo = ttk.Label(self.info_frame, text="Cargo: ")
        self.lbl_cargo.grid(row=1, column=0, padx=5, pady=2, sticky='w')
        
        self.lbl_horario = ttk.Label(self.info_frame, text="Horário: ")
        self.lbl_horario.grid(row=2, column=0, padx=5, pady=2, sticky='w')
        
        # Histórico de registros
        historico_frame = ttk.LabelFrame(frame, text="Histórico de Registros")
        historico_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')
        
        columns = ("data", "hora", "tipo")
        self.tree = ttk.Treeview(historico_frame, columns=columns, show="headings", height=8)
        
        self.tree.heading("data", text="Data")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("tipo", text="Tipo")
        
        self.tree.column("data", width=100, anchor='center')
        self.tree.column("hora", width=80, anchor='center')
        self.tree.column("tipo", width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(historico_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        historico_frame.columnconfigure(0, weight=1)
        historico_frame.rowconfigure(0, weight=1)
        
        # Configurar pesos
        frame.columnconfigure(1, weight=1)
        self.info_frame.columnconfigure(0, weight=1)
        historico_frame.columnconfigure(0, weight=1)
        historico_frame.rowconfigure(0, weight=1)

    def registrar_ponto(self):
        codigo = self.codigo_registro_var.get().strip()
        if not codigo:
            messagebox.showerror("Erro", "Digite o código do funcionário!")
            return
        
        # Encontrar funcionário pelo código
        funcionario = None
        for mat, dados in self.dados_funcionarios.items():
            if dados.get('codigo_ponto') == codigo:
                funcionario = dados
                matricula = mat
                break
        
        if not funcionario:
            messagebox.showerror("Erro", "Código inválido ou não encontrado!")
            return
        
        # Atualizar informações do funcionário
        self.lbl_nome.config(text=f"Nome: {funcionario['nome']}")
        self.lbl_cargo.config(text=f"Cargo: {funcionario.get('cargo', 'Não informado')}")
        
        # Carregar horário se existir
        horario = self.horarios_config.get(matricula, {})
        if horario:
            horario_text = f"Entrada: {horario.get('entrada', '')} | Saída: {horario.get('saída', '')}"
            self.lbl_horario.config(text=f"Horário: {horario_text}")
        
        # Registrar ponto
        agora = datetime.datetime.now()
        data_str = agora.strftime("%d/%m/%Y")
        hora_str = agora.strftime("%H:%M:%S")
        
        # Determinar tipo de registro
        registros_hoje = [r for r in self.registros_ponto.get(matricula, []) 
                         if r['data'] == data_str]
        
        tipos = ["Entrada", "Saída Almoço", "Retorno Almoço", "Saída", "Café", "Hora Extra"]
        
        if not registros_hoje:
            tipo = "Entrada"
        else:
            # Encontrar o próximo tipo de registro
            ultimo_tipo = registros_hoje[-1]['tipo']
            if ultimo_tipo == "Entrada":
                tipo = "Saída Almoço" if "saída_almoço" in horario else "Saída"
            elif ultimo_tipo == "Saída Almoço":
                tipo = "Retorno Almoço"
            elif ultimo_tipo == "Retorno Almoço":
                tipo = "Saída"
            elif ultimo_tipo == "Saída":
                tipo = "Hora Extra"
            else:
                tipo = "Hora Extra"  # Continuar registrando horas extras
        
        # Adicionar registro
        registro = {
            "data": data_str,
            "hora": hora_str,
            "tipo": tipo
        }
        
        if matricula not in self.registros_ponto:
            self.registros_ponto[matricula] = []
        
        self.registros_ponto[matricula].append(registro)
        
        # Atualizar treeview
        self.tree.insert("", "end", values=(data_str, hora_str, tipo))
        
        # Rolagem automática para o final
        self.tree.yview_moveto(1)
        
        # Feedback visual
        messagebox.showinfo("Ponto Registrado", f"{tipo} registrado às {hora_str}")
        
        # Limpar campo de código
        self.codigo_registro_var.set("")