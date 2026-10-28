import psycopg2

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

conexao = psycopg2.connect(URL_NEON)
cursor = conexao.cursor()

# Atualiza a coluna 'comprado' para 1 (Verdadeiro) onde o nome for 'Queijo Mussarela'
cursor.execute("UPDATE itens SET comprado = 1 WHERE nome = %s", ('Queijo Mussarela',))

conexao.commit()
conexao.close()

print("Queijo Mussarela ticado como comprado!")