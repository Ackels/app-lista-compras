import sqlite3

conexao = sqlite3.connect('compras.db')
cursor = conexao.cursor()

# Adiciona a coluna 'preco' do tipo REAL (que aceita números com vírgula/decimais)
cursor.execute("ALTER TABLE itens ADD COLUMN preco REAL DEFAULT 0.0")

conexao.commit()
conexao.close()

print("Coluna de preço adicionada com sucesso!")