import psycopg2

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

conexao = psycopg2.connect(URL_NEON)
cursor = conexao.cursor()

# Adiciona a coluna 'preco' do tipo REAL (que aceita números com vírgula/decimais)
cursor.execute("ALTER TABLE itens ADD COLUMN preco REAL DEFAULT 0.0")

conexao.commit()
conexao.close()

print("Coluna de preço adicionada com sucesso!")