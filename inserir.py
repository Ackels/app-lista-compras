import psycopg2

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

conexao = psycopg2.connect(URL_NEON)
cursor = conexao.cursor()

# O PostgreSQL usa %s para os parâmetros
cursor.execute("INSERT INTO categorias (nome) VALUES (%s)", ('Laticínios',))
cursor.execute("INSERT INTO categorias (nome) VALUES (%s)", ('Limpeza',))
cursor.execute("INSERT INTO categorias (nome) VALUES (%s)", ('Hortifruti',))

cursor.execute('''
    INSERT INTO itens (nome, quantidade, comprado, categoria_id) 
    VALUES (%s, %s, %s, %s)
''', ('Queijo Mussarela', 1, False, 1)) # PostgreSQL usa False/True para booleanos

cursor.execute('''
    INSERT INTO itens (nome, quantidade, comprado, categoria_id) 
    VALUES (%s, %s, %s, %s)
''', ('Detergente', 3, False, 2))

conexao.commit()
conexao.close()

print("Categorias e itens inseridos com sucesso!")