import sqlite3
import os

DB_DIR = r"C:\Users\998096\Documents\python\PROJETO_TURMA_RH_SENAC\DATA"
DB_PATH = os.path.join(DB_DIR, 'database.db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

def popula_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Inserção na tabela cadastros
    cursor.executemany('''
        INSERT OR IGNORE INTO cadastros (nome, matricula, contato, idade, data_nascimento, cpf, rg, tipo_contratacao, cargo, salario, data_admissao, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', [
        ('Administrador 1', 1001, 11999990001, 35, '1989-04-10', 12345678901, 1234567, 'Fixa', 'ADM', 7000.00, '2020-01-15', 'Sim'),
        ('Administrador 2', 1002, 11999990002, 40, '1984-07-22', 12345678902, 1234568, 'Fixa', 'ADM', 7500.00, '2019-08-20', 'Sim'),
        ('Administrador 3', 1003, 11999990003, 38, '1986-03-11', 12345678903, 1234569, 'Fixa', 'ADM', 7200.00, '2021-03-30', 'Sim'),

        ('Usuário 1', 2001, 11999990011, 28, '1995-01-05', 22345678901, 2234567, 'Horista', 'Técnico', 3000.00, '2023-05-01', 'Sim'),
        ('Usuário 2', 2002, 11999990012, 32, '1991-06-16', 22345678902, 2234568, 'Horista', 'Assistente', 3200.00, '2022-11-12', 'Sim'),
        ('Usuário 3', 2003, 11999990013, 29, '1994-09-21', 22345678903, 2234569, 'Fixa', 'Analista', 4000.00, '2022-03-14', 'Sim'),
        ('Usuário 4', 2004, 11999990014, 27, '1996-12-08', 22345678904, 2234570, 'Fixa', 'Assistente', 3100.00, '2023-01-19', 'Sim'),
        ('Usuário 5', 2005, 11999990015, 31, '1992-07-30', 22345678905, 2234571, 'Horista', 'Técnico', 2900.00, '2023-06-25', 'Sim'),
        ('Usuário 6', 2006, 11999990016, 26, '1997-10-14', 22345678906, 2234572, 'Fixa', 'Analista', 4200.00, '2021-12-05', 'Sim'),
        ('Usuário 7', 2007, 11999990017, 33, '1990-11-02', 22345678907, 2234573, 'Horista', 'Assistente', 3100.00, '2020-10-10', 'Sim'),
        ('Usuário 8', 2008, 11999990018, 30, '1993-05-25', 22345678908, 2234574, 'Fixa', 'Analista', 4100.00, '2022-07-07', 'Sim'),
        ('Usuário 9', 2009, 11999990019, 34, '1989-08-15', 22345678909, 2234575, 'Horista', 'Técnico', 3000.00, '2021-04-22', 'Sim'),
        ('Usuário 10', 2010, 11999990020, 28, '1995-02-20', 22345678910, 2234576, 'Fixa', 'Assistente', 3100.00, '2023-02-14', 'Sim'),
        ('Usuário 11', 2011, 11999990021, 29, '1994-06-06', 22345678911, 2234577, 'Horista', 'Técnico', 2900.00, '2022-09-18', 'Sim'),
        ('Usuário 12', 2012, 11999990022, 27, '1996-03-29', 22345678912, 2234578, 'Fixa', 'Analista', 4200.00, '2023-01-01', 'Sim'),
        ('Usuário 13', 2013, 11999990023, 31, '1992-12-12', 22345678913, 2234579, 'Horista', 'Assistente', 3000.00, '2021-08-08', 'Sim'),
        ('Usuário 14', 2014, 11999990024, 26, '1997-04-18', 22345678914, 2234580, 'Fixa', 'Analista', 4300.00, '2022-05-20', 'Sim'),
        ('Usuário 15', 2015, 11999990025, 32, '1990-09-09', 22345678915, 2234581, 'Horista', 'Técnico', 3100.00, '2020-11-11', 'Sim')
    ])

    # Inserção na tabela usuarios
    cursor.executemany('''
        INSERT OR IGNORE INTO usuarios (matricula, senha, cargo)
        VALUES (?, ?, ?)
    ''', [
        (1001, 'senha1001', 'ADM'),
        (1002, 'senha1002', 'ADM'),
        (1003, 'senha1003', 'ADM'),

        (2001, 'senha2001', 'USER'),
        (2002, 'senha2002', 'USER'),
        (2003, 'senha2003', 'USER'),
        (2004, 'senha2004', 'USER'),
        (2005, 'senha2005', 'USER'),
        (2006, 'senha2006', 'USER'),
        (2007, 'senha2007', 'USER'),
        (2008, 'senha2008', 'USER'),
        (2009, 'senha2009', 'USER'),
        (2010, 'senha2010', 'USER'),
        (2011, 'senha2011', 'USER'),
        (2012, 'senha2012', 'USER'),
        (2013, 'senha2013', 'USER'),
        (2014, 'senha2014', 'USER'),
        (2015, 'senha2015', 'USER')
    ])

    conn.commit()
    conn.close()
    print("Dados fictícios inseridos com sucesso!")

if __name__ == "__main__":
    popula_banco()
