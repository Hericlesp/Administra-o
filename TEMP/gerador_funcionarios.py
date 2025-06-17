import sqlite3
import os
import random
from datetime import datetime, timedelta
from faker import Faker
from unidecode import unidecode

class GeradorBaseDados:
    def __init__(self, db_dir, num_funcionarios=25):
        self.db_dir = db_dir
        self.db_path = os.path.join(db_dir, 'database.db')
        self.num_funcionarios = num_funcionarios
        self.fake = Faker('pt_BR')
        
        # Criar diretório se não existir
        os.makedirs(db_dir, exist_ok=True)
        
        # Conectar ao banco de dados
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Criar tabelas
        self.criar_tabelas()

    def criar_tabelas(self):
        """Cria todas as tabelas necessárias se não existirem"""
        # Tabela principal de funcionários
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS funcionarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_funcionario TEXT NOT NULL,
                matricula_siape INTEGER UNIQUE NOT NULL,
                cargo TEXT NOT NULL,
                funcao TEXT,
                orgao TEXT,
                lotacao TEXT,
                data_exercicio TEXT,
                tipo_contratacao TEXT,
                jornada_trabalho TEXT,
                telefone_corp TEXT,
                email_corp TEXT,
                chefe_imediato TEXT,
                observacoes TEXT,
                
                nome_completo TEXT,
                nome_social TEXT,
                cpf TEXT UNIQUE NOT NULL,
                rg TEXT,
                data_nascimento TEXT,
                estado_civil TEXT,
                naturalidade TEXT,
                nacionalidade TEXT,
                endereco_residencial TEXT,
                telefone_pessoal TEXT,
                email_pessoal TEXT,
                
                caminho_imagem TEXT
            )
        ''')

        # Tabela de dependentes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dependentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcionario_id INTEGER NOT NULL,
                nome TEXT NOT NULL,
                parentesco TEXT,
                data_nascimento TEXT,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de cursos do funcionário
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cursos_funcionario (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcionario_id INTEGER NOT NULL,
                curso TEXT NOT NULL,
                instituicao TEXT,
                carga_horaria INTEGER,
                ano_conclusao INTEGER,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de experiências
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS experiencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcionario_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
            )
        ''')

        # Tabela de competências
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS competencias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcionario_id INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    def gerar_cpf(self):
        """Gera um CPF válido formatado"""
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        # Cálculo do primeiro dígito verificador
        soma = sum(x * y for x, y in zip(cpf, range(10, 1, -1)))
        digito1 = (soma * 10) % 11
        digito1 = digito1 if digito1 < 10 else 0
        cpf.append(digito1)
        
        # Cálculo do segundo dígito verificador
        soma = sum(x * y for x, y in zip(cpf, range(11, 1, -1)))
        digito2 = (soma * 10) % 11
        digito2 = digito2 if digito2 < 10 else 0
        cpf.append(digito2)
        
        return ''.join(map(str, cpf))

    def gerar_data(self, min_anos=0, max_anos=0):
        """Gera uma data aleatória dentro de um intervalo de anos"""
        data_inicio = datetime.now() - timedelta(days=max_anos*365)
        data_fim = datetime.now() - timedelta(days=min_anos*365)
        return self.fake.date_between(data_inicio, data_fim).strftime('%d/%m/%Y')

    def gerar_telefone(self):
        """Gera um número de telefone formatado"""
        return f"({random.randint(11, 99)}) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

    def gerar_email(self, nome, corporativo=True):
        """Gera um e-mail baseado no nome"""
        partes = unidecode(nome.lower()).split()
        base = f"{partes[0]}.{partes[-1]}"
        dominio = self.fake.free_email_domain() if not corporativo else "gov.br"
        return f"{base}@{dominio}"

    def gerar_endereco_completo(self):
        """Gera um endereço completo formatado"""
        logradouro = self.fake.street_name()
        numero = str(random.randint(1, 9999))
        complemento = random.choice(['', 'Casa', f'Apto {random.randint(1, 500)}', 'Sobrado'])
        bairro = self.fake.bairro()
        cidade = self.fake.city()
        estado = self.fake.estado_sigla()
        cep = self.fake.postcode()
        
        return f"{logradouro}, {numero} {complemento} - {bairro}, {cidade} - {estado}, {cep}"

    def gerar_funcionario(self):
        """Gera dados completos de um funcionário"""
        nome_completo = self.fake.name()
        data_nascimento = self.gerar_data(min_anos=18, max_anos=65)
        cpf = self.gerar_cpf()
        rg = ''.join(str(random.randint(0, 9)) for _ in range(9))
        
        # Dados profissionais
        cargos = [
            'Analista de TI', 'Desenvolvedor', 'Gerente de Projetos', 
            'Assistente Administrativo', 'Contador', 'Recrutador',
            'Engenheiro Civil', 'Designer Gráfico', 'Analista de Marketing',
            'Professor', 'Coordenador Pedagógico', 'Secretário Escolar'
        ]
        
        orgaos = [
            'Secretaria de Educação', 'Prefeitura Municipal', 
            'Governo do Estado', 'Ministério da Educação'
        ]
        
        lotacoes = [
            'TI', 'RH', 'Financeiro', 'Administrativo', 'Compras',
            'Pedagogia', 'Coordenação', 'Diretoria'
        ]
        
        cargo = random.choice(cargos)
        funcao = cargo  # Simplificação
        orgao = random.choice(orgaos)
        lotacao = random.choice(lotacoes)
        data_exercicio = self.gerar_data(min_anos=0, max_anos=10)
        tipo_contratacao = random.choice(['CLT', 'Estagiário', 'PJ', 'Comissionado'])
        jornada_trabalho = random.choice(['40h semanais', '30h semanais', '44h semanais'])
        
        telefone_corp = self.gerar_telefone()
        email_corp = self.gerar_email(nome_completo)
        chefe_imediato = self.fake.name()
        observacoes = random.choice(['', 'Alto desempenho', 'Promoção pendente', 'Treinamento necessário'])
        
        # Dados pessoais
        nome_social = ''
        if random.random() < 0.1:  # 10% chance de ter nome social
            nome_social = self.fake.first_name()
        
        estado_civil = random.choice(['Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)'])
        naturalidade = self.fake.city()
        nacionalidade = 'Brasileiro'
        endereco_residencial = self.gerar_endereco_completo()
        telefone_pessoal = self.gerar_telefone()
        email_pessoal = self.gerar_email(nome_completo, corporativo=False)
        
        # Gerar matrícula no formato SIAPE (5-8 dígitos)
        matricula_siape = str(random.randint(10000, 99999999))
        
        return {
            'nome_funcionario': nome_completo,
            'matricula_siape': matricula_siape,
            'cargo': cargo,
            'funcao': funcao,
            'orgao': orgao,
            'lotacao': lotacao,
            'data_exercicio': data_exercicio,
            'tipo_contratacao': tipo_contratacao,
            'jornada_trabalho': jornada_trabalho,
            'telefone_corp': telefone_corp,
            'email_corp': email_corp,
            'chefe_imediato': chefe_imediato,
            'observacoes': observacoes,
            'nome_completo': nome_completo,
            'nome_social': nome_social,
            'cpf': cpf,
            'rg': rg,
            'data_nascimento': data_nascimento,
            'estado_civil': estado_civil,
            'naturalidade': naturalidade,
            'nacionalidade': nacionalidade,
            'endereco_residencial': endereco_residencial,
            'telefone_pessoal': telefone_pessoal,
            'email_pessoal': email_pessoal,
            'caminho_imagem': ''
        }

    def gerar_dependente(self):
        """Gera dados de um dependente"""
        parentescos = ['Filho(a)', 'Cônjuge', 'Enteado(a)', 'Neto(a)', 'Pai/Mãe']
        return {
            'nome': self.fake.name(),
            'parentesco': random.choice(parentescos),
            'data_nascimento': self.gerar_data(min_anos=0, max_anos=30)
        }

    def gerar_curso(self):
        """Gera dados de um curso"""
        cursos = [
            'Graduação em Administração', 'Pós-graduação em Gestão Pública',
            'Curso de Informática Básica', 'Formação em Pedagogia',
            'MBA em Gestão de Projetos', 'Curso de Liderança',
            'Especialização em RH', 'Curso de Excel Avançado'
        ]
        
        instituicoes = [
            'UFMG', 'PUC', 'UNESP', 'USP', 'UNICAMP',
            'SENAC', 'SENAI', 'FGV', 'Fundação Bradesco'
        ]
        
        return {
            'curso': random.choice(cursos),
            'instituicao': random.choice(instituicoes),
            'carga_horaria': random.randint(40, 400),
            'ano_conclusao': random.randint(2000, 2023)
        }

    def gerar_experiencia(self):
        """Gera uma descrição de experiência profissional"""
        experiencias = [
            'Desenvolvimento de sistemas educacionais',
            'Gestão de equipes pedagógicas',
            'Implementação de projetos de TI',
            'Coordenação de programas educacionais',
            'Recrutamento e seleção de profissionais',
            'Gestão financeira de departamentos',
            'Planejamento estratégico institucional',
            'Treinamento e desenvolvimento de equipes'
        ]
        return {'descricao': random.choice(experiencias)}

    def gerar_competencia(self):
        """Gera uma descrição de competência"""
        competencias = [
            'Liderança de equipes', 'Comunicação eficaz', 
            'Gestão de projetos', 'Conhecimento em informática',
            'Planejamento estratégico', 'Resolução de problemas',
            'Trabalho em equipe', 'Atendimento ao público',
            'Conhecimento em legislação educacional',
            'Fluência em inglês', 'Habilidades em Excel'
        ]
        return {'descricao': random.choice(competencias)}

    def inserir_funcionario(self, funcionario):
        """Insere um funcionário no banco e retorna seu ID"""
        try:
            self.cursor.execute('''
                INSERT INTO funcionarios (
                    nome_funcionario, matricula_siape, cargo, funcao, orgao, lotacao,
                    data_exercicio, tipo_contratacao, jornada_trabalho, telefone_corp, email_corp,
                    chefe_imediato, observacoes, nome_completo, nome_social, cpf, rg,
                    data_nascimento, estado_civil, naturalidade, nacionalidade, endereco_residencial,
                    telefone_pessoal, email_pessoal, caminho_imagem
                ) VALUES (
                    :nome_funcionario, :matricula_siape, :cargo, :funcao, :orgao, :lotacao,
                    :data_exercicio, :tipo_contratacao, :jornada_trabalho, :telefone_corp, :email_corp,
                    :chefe_imediato, :observacoes, :nome_completo, :nome_social, :cpf, :rg,
                    :data_nascimento, :estado_civil, :naturalidade, :nacionalidade, :endereco_residencial,
                    :telefone_pessoal, :email_pessoal, :caminho_imagem
                )
            ''', funcionario)
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            print(f"Erro de integridade: {e}")
            return None
        except Exception as e:
            print(f"Erro ao inserir funcionário: {e}")
            return None

    def inserir_dependentes(self, funcionario_id, num_dependentes):
        """Insere dependentes para um funcionário"""
        for _ in range(num_dependentes):
            dependente = self.gerar_dependente()
            self.cursor.execute('''
                INSERT INTO dependentes (
                    funcionario_id, nome, parentesco, data_nascimento
                ) VALUES (?, ?, ?, ?)
            ''', (funcionario_id, dependente['nome'], dependente['parentesco'], dependente['data_nascimento']))

    def inserir_cursos(self, funcionario_id, num_cursos):
        """Insere cursos para um funcionário"""
        for _ in range(num_cursos):
            curso = self.gerar_curso()
            self.cursor.execute('''
                INSERT INTO cursos_funcionario (
                    funcionario_id, curso, instituicao, carga_horaria, ano_conclusao
                ) VALUES (?, ?, ?, ?, ?)
            ''', (funcionario_id, curso['curso'], curso['instituicao'], curso['carga_horaria'], curso['ano_conclusao']))

    def inserir_experiencias(self, funcionario_id, num_experiencias):
        """Insere experiências para um funcionário"""
        for _ in range(num_experiencias):
            experiencia = self.gerar_experiencia()
            self.cursor.execute('''
                INSERT INTO experiencias (
                    funcionario_id, descricao
                ) VALUES (?, ?)
            ''', (funcionario_id, experiencia['descricao']))

    def inserir_competencias(self, funcionario_id, num_competencias):
        """Insere competências para um funcionário"""
        for _ in range(num_competencias):
            competencia = self.gerar_competencia()
            self.cursor.execute('''
                INSERT INTO competencias (
                    funcionario_id, descricao
                ) VALUES (?, ?)
            ''', (funcionario_id, competencia['descricao']))

    def gerar_base_completa(self):
        """Gera todos os dados para o banco de dados"""
        sucessos = 0
        tentativas = 0
        max_tentativas = self.num_funcionarios * 2
        
        while sucessos < self.num_funcionarios and tentativas < max_tentativas:
            tentativas += 1
            funcionario = self.gerar_funcionario()
            funcionario_id = self.inserir_funcionario(funcionario)
            
            if funcionario_id:
                sucessos += 1
                print(f"Funcionário {sucessos}/{self.num_funcionarios} inserido (ID: {funcionario_id})")
                
                # Gerar dados relacionados
                self.inserir_dependentes(funcionario_id, random.randint(0, 4))
                self.inserir_cursos(funcionario_id, random.randint(1, 5))
                self.inserir_experiencias(funcionario_id, random.randint(1, 5))
                self.inserir_competencias(funcionario_id, random.randint(3, 8))
        
        self.conn.commit()
        return sucessos

    def fechar_conexao(self):
        """Fecha a conexão com o banco de dados"""
        self.conn.close()

if __name__ == "__main__":
    # Configurações
    DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
    NUM_FUNCIONARIOS = 25
    
    # Criar e executar gerador
    print(f"Gerando dados no caminho: {DB_DIR}")
    gerador = GeradorBaseDados(DB_DIR, NUM_FUNCIONARIOS)
    sucessos = gerador.gerar_base_completa()
    gerador.fechar_conexao()
    
    print(f"\n{sucessos} funcionários fictícios gerados com sucesso!")
    print(f"Com todos os dados relacionados (dependentes, cursos, experiências, competências)")
    print(f"Banco de dados atualizado em: {gerador.db_path}")