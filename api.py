from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Meu App de Compras")

# Configuração de Segurança (CORS) para permitir que o HTML converse com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NovoItem(BaseModel):
    nome: str
    categoria_id: int
    preco: float = 0.0

@app.get("/categorias")
def listar_categorias():
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categorias")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista_categorias = []
    for linha in resultados:
        lista_categorias.append({"id": linha[0], "nome": linha[1]})
    return lista_categorias

@app.post("/itens")
def adicionar_item(item: NovoItem):
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO itens (nome, quantidade, comprado, categoria_id, preco) VALUES (?, 1, 0, ?, ?)",
        (item.nome, item.categoria_id, item.preco)
    )
    conexao.commit()
    conexao.close()
    return {"mensagem": f"O item '{item.nome}' foi adicionado com sucesso!"}

# --- A ROTA QUE PROVAVELMENTE FULTOU ---
@app.get("/itens")
def listar_itens():
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    cursor.execute('''
        SELECT itens.id, itens.nome, itens.quantidade, categorias.nome, itens.comprado, itens.preco
        FROM itens
        JOIN categorias ON itens.categoria_id = categorias.id
    ''')
    resultados = cursor.fetchall()
    conexao.close()
    
    lista_itens = []
    for linha in resultados:
        lista_itens.append({
            "id": linha[0],
            "nome": linha[1],
            "quantidade": linha[2],
            "categoria": linha[3],
            "comprado": bool(linha[4]),
            "preco": linha[5]  # Adicionamos o preço aqui!
        })
    return lista_itens

@app.put("/itens/{item_id}")
def alternar_item(item_id: int):
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    
    # 1. Primeiro, perguntamos ao banco qual é o status atual deste item
    cursor.execute("SELECT comprado FROM itens WHERE id = ?", (item_id,))
    status_atual = cursor.fetchone()[0]
    
    # 2. Se for 1, vira 0. Se for 0, vira 1 (Lógica de "interruptor")
    novo_status = 0 if status_atual == 1 else 1
    
    # 3. Atualizamos o banco com o novo status
    cursor.execute("UPDATE itens SET comprado = ? WHERE id = ?", (novo_status, item_id))
    conexao.commit()
    conexao.close()
    
    return {"mensagem": f"Status do item {item_id} alterado!"}


# NOVA ROTA: O verbo DELETE é o padrão na internet para apagar coisas
@app.delete("/itens/{item_id}")
def deletar_item(item_id: int):
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    
    # Apaga do banco onde o ID for igual ao enviado
    cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()
    
    return {"mensagem": "Item excluído com sucesso!"}

# Rota para AUMENTAR a quantidade
@app.put("/itens/{item_id}/aumentar")
def aumentar_quantidade(item_id: int):
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    # Pega o valor atual e soma 1
    cursor.execute("UPDATE itens SET quantidade = quantidade + 1 WHERE id = ?", (item_id,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Quantidade aumentada"}

# Rota para DIMINUIR a quantidade
@app.put("/itens/{item_id}/diminuir")
def diminuir_quantidade(item_id: int):
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    # Subtrai 1, mas a regra "AND quantidade > 1" impede que a quantidade fique zero ou negativa
    cursor.execute("UPDATE itens SET quantidade = quantidade - 1 WHERE id = ? AND quantidade > 1", (item_id,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Quantidade diminuída"}

@app.delete("/itens-comprados")
def limpar_comprados():
    conexao = sqlite3.connect('compras.db')
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM itens WHERE comprado = 1")
    conexao.commit()
    conexao.close()
    return {"mensagem": "Itens comprados foram removidos!"}




# python -m uvicorn api:app --reload