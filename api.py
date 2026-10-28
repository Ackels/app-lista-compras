from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Meu App de Compras")

URL_NEON = "postgresql://neondb_owner:npg_9Zri4VAtomkM@ep-purple-dawn-b6x9hc07-pooler.c-2.sa-east-1.aws.neon.tech/neondb?sslmode=require"

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
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categorias ORDER BY id ASC")
    resultados = cursor.fetchall()
    conexao.close()
    
    lista_categorias = []
    for linha in resultados:
        lista_categorias.append({"id": linha[0], "nome": linha[1]})
    return lista_categorias

@app.post("/itens")
def adicionar_item(item: NovoItem):
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO itens (nome, quantidade, comprado, categoria_id, preco) VALUES (%s, 1, FALSE, %s, %s)",
        (item.nome, item.categoria_id, item.preco)
    )
    conexao.commit()
    conexao.close()
    return {"mensagem": f"O item '{item.nome}' foi adicionado com sucesso!"}

@app.get("/itens")
def listar_itens():
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    # Adicionado ORDER BY itens.id ASC para fixar a ordem da lista na tela
    cursor.execute('''
        SELECT itens.id, itens.nome, itens.quantidade, categorias.nome, itens.comprado, itens.preco
        FROM itens
        JOIN categorias ON itens.categoria_id = categorias.id
        ORDER BY itens.id ASC
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
            "preco": float(linha[5]) if linha[5] is not None else 0.0
        })
    return lista_itens

@app.put("/itens/{item_id}")
def alternar_item(item_id: int):
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    
    cursor.execute("SELECT comprado FROM itens WHERE id = %s", (item_id,))
    linha = cursor.fetchone()
    if not linha:
        conexao.close()
        return {"erro": "Item não encontrado"}
        
    status_atual = linha[0]
    # Alterna valor booleano nativo do PostgreSQL
    novo_status = not bool(status_atual)
    
    cursor.execute("UPDATE itens SET comprado = %s WHERE id = %s", (novo_status, item_id))
    conexao.commit()
    conexao.close()
    
    return {"mensagem": f"Status do item {item_id} alterado!"}

@app.delete("/itens/{item_id}")
def deletar_item(item_id: int):
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM itens WHERE id = %s", (item_id,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Item excluído com sucesso!"}

@app.put("/itens/{item_id}/aumentar")
def aumentar_quantidade(item_id: int):
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute("UPDATE itens SET quantidade = quantidade + 1 WHERE id = %s", (item_id,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Quantidade aumentada"}

@app.put("/itens/{item_id}/diminuir")
def diminuir_quantidade(item_id: int):
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute("UPDATE itens SET quantidade = quantidade - 1 WHERE id = %s AND quantidade > 1", (item_id,))
    conexao.commit()
    conexao.close()
    return {"mensagem": "Quantidade diminuída"}

@app.delete("/itens-comprados")
def limpar_comprados():
    conexao = psycopg2.connect(URL_NEON)
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM itens WHERE comprado = TRUE")
    conexao.commit()
    conexao.close()
    return {"mensagem": "Itens comprados foram removidos!"}