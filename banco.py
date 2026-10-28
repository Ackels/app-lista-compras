import psycopg2

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

conexao = psycopg2.connect(URL_NEON)
cursor = conexao.cursor()

# Cria a tabela de categorias
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL
)
''')

# Cria a tabela de itens JÁ COM A COLUNA DE PREÇO
cursor.execute('''
CREATE TABLE IF NOT EXISTS itens (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    quantidade INTEGER DEFAULT 1,
    comprado BOOLEAN DEFAULT FALSE,
    preco REAL DEFAULT 0.0,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
)
''')

# Insere as categorias de teste
cursor.execute("INSERT INTO categorias (nome) VALUES ('Laticínios'), ('Limpeza'), ('Hortifruti'), ('Carnes')")

conexao.commit()
conexao.close()

print("Banco criado com sucesso na nuvem Neon, agora com a coluna PRECO!")