import sqlite3

conexao = sqlite3.connect('compras.db')
cursor = conexao.cursor()

# Cria a tabela de categorias
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

# Cria a tabela de itens JÁ COM A COLUNA DE PREÇO
cursor.execute('''
CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER DEFAULT 1,
    comprado BOOLEAN DEFAULT 0,
    preco REAL DEFAULT 0.0,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
)
''')

# Insere as categorias de teste
cursor.execute("INSERT INTO categorias (nome) VALUES ('Laticínios'), ('Limpeza'), ('Hortifruti'), ('Carnes')")

conexao.commit()
conexao.close()

print("Banco criado com sucesso, agora com a coluna PRECO!")