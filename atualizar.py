import sqlite3

conexao = sqlite3.connect('compras.db')
cursor = conexao.cursor()

# Atualiza a coluna 'comprado' para 1 (Verdadeiro) onde o nome for 'Queijo Mussarela'
cursor.execute("UPDATE itens SET comprado = 1 WHERE nome = ?", ('Queijo Mussarela',))

conexao.commit()
conexao.close()

print("Queijo Mussarela ticado como comprado!")