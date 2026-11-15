import sqlite3

conexao = sqlite3.connect('compras.db')
cursor = conexao.cursor()

# 1. Inserindo as Categorias
# O id é gerado automaticamente pelo AUTOINCREMENT, então só enviamos o nome.
# Usamos o símbolo (?) como boa prática de segurança (evita SQL Injection).
cursor.execute("INSERT INTO categorias (nome) VALUES (?)", ('Laticínios',))
cursor.execute("INSERT INTO categorias (nome) VALUES (?)", ('Limpeza',))
cursor.execute("INSERT INTO categorias (nome) VALUES (?)", ('Hortifruti',))

# 2. Inserindo os Itens
# Como inserimos Laticínios primeiro, o ID dela no banco é 1. Limpeza é 2. Hortifruti é 3.
cursor.execute('''
    INSERT INTO itens (nome, quantidade, comprado, categoria_id) 
    VALUES (?, ?, ?, ?)
''', ('Queijo Mussarela', 1, 0, 1)) # 1 unidade, 0 (não comprado), categoria 1

cursor.execute('''
    INSERT INTO itens (nome, quantidade, comprado, categoria_id) 
    VALUES (?, ?, ?, ?)
''', ('Detergente', 3, 0, 2)) # 3 unidades, 0 (não comprado), categoria 2

# 3. Salvando as alterações
conexao.commit()
conexao.close()

print("Categorias e itens inseridos com sucesso!")