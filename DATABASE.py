# import sqlite3
# import os

# # Caminho do banco
# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')

# # Caminho do banco
# DB_DIR = r"\\educcur03\Users\Public\DJANGO\Administração\DATA"
# DB_PATH = os.path.join(DB_DIR, 'database.db')

# # Criação da pasta, se não existir
# if not os.path.exists(DB_DIR):
#     os.makedirs(DB_DIR)


# def criar_banco_e_tabelas():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # 🏛️ Tabela de cadastro dos funcionários
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS cadastros (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             matricula INTEGER UNIQUE NOT NULL,
#             contato INTEGER,
#             idade INTEGER,
#             data_nascimento TEXT,
#             cpf INTEGER,
#             rg INTEGER,
#             tipo_contratacao TEXT CHECK (tipo_contratacao IN ('Fixa', 'Horista')),
#             cargo TEXT,
#             salario REAL,
#             data_admissao TEXT,
#             ativo TEXT CHECK (ativo IN ('Sim', 'Não')) DEFAULT 'Sim'
#         )
#     ''')

#     # 🕒 Tabela de registro de ponto
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS registro_ponto (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             colaborador_id INTEGER,
#             data TEXT,
#             hora TEXT,
#             tipo TEXT CHECK (tipo IN ('Entrada', 'Saída')),
#             FOREIGN KEY (colaborador_id) REFERENCES cadastros(id)
#         )
#     ''')

#     # 🗂️ Tabela de códigos gerados (HISTÓRICO COMPLETO DOS CÓDIGOS)
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS registros_codigos (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             colaborador_id INTEGER,
#             data TEXT,
#             hora TEXT,
#             codigo TEXT,
#             tipo TEXT CHECK (tipo IN ('Entrada', 'Almoço', 'Retorno', 'Saída')),
#             status TEXT CHECK (status IN ('Ativo', 'Expirado')) DEFAULT 'Ativo',
#             FOREIGN KEY (colaborador_id) REFERENCES cadastros(id)
#         )
#     ''')

#     # 👤 Tabela de usuários (login de acesso ao sistema)
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS usuarios (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             matricula INTEGER UNIQUE NOT NULL,
#             senha TEXT NOT NULL,
#             cargo TEXT CHECK (cargo IN ('ADM', 'USER', 'ROOT')) NOT NULL
#         )
#     ''')

#     # 🔧 Inserir usuário administrador padrão, se não existir
#     cursor.execute('SELECT * FROM usuarios WHERE matricula = ?', (998096,))
#     if not cursor.fetchone():
#         cursor.execute('''
#             INSERT INTO usuarios (matricula, senha, cargo)
#             VALUES (?, ?, ?)
#         ''', (998096, '998096', 'ROOT'))

#     conn.commit()
#     conn.close()
#     print('Banco de dados e tabelas criadas/verificadas com sucesso!')


# # Executa a criação do banco sempre que roda
# criar_banco_e_tabelas()


import sqlite3
import os

# Caminho do banco
DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

# Criação da pasta, se não existir
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)


def criar_banco_e_tabelas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela principal de funcionários
    cursor.execute('''
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
    cursor.execute('''
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
    cursor.execute('''
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS experiencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de competências
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS competencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            funcionario_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print('Banco de dados e tabelas criadas/verificadas com sucesso!')


# Executa a criação do banco e tabelas
criar_banco_e_tabelas()
