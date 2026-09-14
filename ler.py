import sqlite3

conexao = sqlite3.connect('compras.db')
cursor = conexao.cursor()

# 1. Fazendo a consulta (Query) cruzando as duas tabelas
cursor.execute('''
    SELECT itens.nome, itens.quantidade, categorias.nome, itens.comprado
    FROM itens
    JOIN categorias ON itens.categoria_id = categorias.id
''')

# 2. Pegando todos os resultados devolvidos pelo banco
resultados = cursor.fetchall()

# 3. Exibindo de forma amigável no terminal
print("--- MINHA LISTA DE COMPRAS ---")
for linha in resultados:
    nome_item = linha[0]
    quantidade = linha[1]
    nome_categoria = linha[2]
    
    # Se for 1, é verdadeiro (comprado). Se for 0, é falso (pendente).
    status = "[x] Comprado" if linha[3] == 1 else "[ ] Pendente"
    
    print(f"{status} | {quantidade}x {nome_item} (Categoria: {nome_categoria})")

conexao.close()