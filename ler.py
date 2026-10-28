import psycopg2

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

conexao = psycopg2.connect(URL_NEON)
cursor = conexao.cursor()

cursor.execute('''
    SELECT itens.nome, itens.quantidade, categorias.nome, itens.comprado
    FROM itens
    JOIN categorias ON itens.categoria_id = categorias.id
''')

resultados = cursor.fetchall()

print("--- MINHA LISTA DE COMPRAS ---")
for linha in resultados:
    nome_item = linha[0]
    quantidade = linha[1]
    nome_categoria = linha[2]
    
    # O PostgreSQL devolve um valor booleano (True/False) em vez de números (1/0)
    status = "[x] Comprado" if linha[3] else "[ ] Pendente"
    
    print(f"{status} | {quantidade}x {nome_item} (Categoria: {nome_categoria})")

conexao.close()