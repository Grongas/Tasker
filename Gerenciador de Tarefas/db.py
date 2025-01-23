import sqlite3

def init_db():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            data_entrega TEXT,
            criador TEXT,
            descricao TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_tarefa_db(nome, data_criacao, data_entrega, criador, descricao):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tarefas (nome, data_criacao, data_entrega, criador, descricao) VALUES (?, ?, ?, ?, ?)''', (nome, data_criacao, data_entrega, criador, descricao))
    conn.commit()
    conn.close()

def remover_tarefa_db(nome):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE nome = ?', (nome,))
    conn.commit()
    conn.close()

def obter_tarefas_db():
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return [tarefa[0] for tarefa in tarefas]

def obter_detalhes_tarefa(nome):
    conn = sqlite3.connect('tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE nome=?', (nome,))
    detalhes = cursor.fetchone()
    conn.close()
    return detalhes