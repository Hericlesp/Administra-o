import sqlite3
import os
import random
from faker import Faker

# Configurar idioma do Faker
fake = Faker('pt_BR')

# Caminho do banco
DB_DIR = r"C:\Users\998096\Documents\python\Administração\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

# Conectar ao banco
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Inserir 25 funcionários fictícios
for _ in range(25):
    dados = {
        'nome': fake.name(),
        'matricula': random.randint(100000, 999999),
        'contato': fake.phone_number(),
        'idade': random.randint(18, 60),
        'data_nascimento': fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%Y-%m-%d'),
        'cpf': fake.cpf(),
        'rg': fake.random_number(digits=9),
        'tipo_contratacao': random.choice(['Fixa', 'Horista']),
        'cargo': random.choice(['ADM', 'USER']),
        'salario': round(random.uniform(2000, 9000), 2),
        'data_admissao': fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
        'ativo': random.choice(['Sim', 'Não']),
        'foto_path': '',

        'filiacao_mae': fake.name_female(),
        'filiacao_pai': fake.name_male(),
        'local_nascimento': fake.city(),
        'nacionalidade': 'Brasileiro(a)',
        'uf_nascimento': fake.estado_sigla(),
        'estado_civil': random.choice(['Solteiro', 'Casado', 'Divorciado']),
        'conjuge': fake.name() if random.choice([True, False]) else '',
        'certidao_casamento': fake.uuid4(),

        'rg_emissao': fake.date(),
        'rg_orgao_emissor': 'SSP',
        'rg_data_emissao': fake.date(),
        'cart_profissional': fake.random_number(digits=6),
        'conselho': '',
        'ctps': fake.random_number(digits=6),
        'ctps_serie': fake.random_number(digits=4),
        'cart_reservista': fake.random_number(digits=5),
        'exame_medico': fake.date(),
        'titulo_eleitor': fake.random_number(digits=12),
        'titulo_zona': fake.random_number(digits=3),
        'titulo_secao': fake.random_number(digits=3),
        'pis_pasep': fake.random_number(digits=11),
        'habilitacao': fake.random_number(digits=11),
        'habilitacao_categoria': random.choice(['A', 'B', 'AB']),
        'habilitacao_vencimento': fake.date_between(start_date='today', end_date='+5y').strftime('%Y-%m-%d'),

        'logradouro': fake.street_name(),
        'numero': str(random.randint(1, 9999)),
        'complemento': '',
        'bairro': fake.bairro(),
        'cidade': fake.city(),
        'cep': fake.postcode(),
        'uf_endereco': fake.estado_sigla(),
        'alteracao_endereco1': '',
        'alteracao_endereco2': '',
        'alteracao_endereco3': '',

        'cor': random.choice(['Branca', 'Parda', 'Negra']),
        'altura': f"{random.uniform(1.5, 1.9):.2f}",
        'peso': str(random.randint(50, 100)),
        'olhos': random.choice(['Castanhos', 'Azuis', 'Verdes']),
        'cabelos': random.choice(['Pretos', 'Castanhos', 'Loiros']),
        'sinais': '',

        'data_chegada_brasil': '',
        'pais_origem': '',
        'carteira_modelo19': '',
        'registro_geral': '',
        'conjuge_estrangeiro': '',
        'quantos_filhos': random.randint(0, 3),
        'conjuge_brasileiro': random.choice(['Sim', 'Não']),
        'filhos_brasileiros': random.choice(['Sim', 'Não']),

        'raca_cor': random.choice(['Branca', 'Parda', 'Negra', 'Amarela']),
        'dependentes': ''
    }

    colunas = ', '.join(dados.keys())
    placeholders = ', '.join(['?'] * len(dados))
    valores = list(dados.values())

    try:
        cursor.execute(f'''
            INSERT INTO funcionarios ({colunas})
            VALUES ({placeholders})
        ''', valores)
    except Exception as e:
        print(f"Erro ao inserir funcionário: {e}")

conn.commit()
conn.close()
print("✅ 25 funcionários fictícios inseridos com sucesso!")
