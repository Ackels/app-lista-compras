from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from banco import conectar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Garante que a tabela de códigos personalizados exista no banco
def inicializar_tabela_produtos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_conhecidos (
            codigo_barras TEXT PRIMARY KEY,
            nome TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

inicializar_tabela_produtos()

class ItemCreate(BaseModel):
    nome: str
    categoria_id: int
    preco: float = 0.0
    codigo_barras: str | None = None

class PrecoUpdate(BaseModel):
    preco: float

@app.get("/categorias")
def listar_categorias():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM categorias ORDER BY id")
    categorias = [{"id": row[0], "nome": row[1]} for row in cursor.fetchall()]
    conn.close()
    return categorias

@app.get("/itens")
def listar_itens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id, i.nome, i.comprado, c.nome, i.preco, i.quantidade
        FROM itens i
        JOIN categorias c ON i.categoria_id = c.id
        ORDER BY i.comprado ASC, i.id DESC
    """)
    itens = [
        {
            "id": row[0],
            "nome": row[1],
            "comprado": bool(row[2]),
            "categoria": row[3],
            "preco": float(row[4] or 0.0),
            "quantidade": int(row[5] or 1)
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return itens

@app.post("/itens")
def criar_item(item: ItemCreate):
    conn = conectar()
    cursor = conn.cursor()
    
    # Se veio um código de barras novo, salva/atualiza na memória do app
    if item.codigo_barras:
        cursor.execute("DELETE FROM produtos_conhecidos WHERE codigo_barras = %s" if hasattr(conn, 'info') else "DELETE FROM produtos_conhecidos WHERE codigo_barras = ?", (item.codigo_barras,))
        cursor.execute("INSERT INTO produtos_conhecidos (codigo_barras, nome) VALUES (%s, %s)" if hasattr(conn, 'info') else "INSERT INTO produtos_conhecidos (codigo_barras, nome) VALUES (?, ?)", (item.codigo_barras, item.nome))

    query = "INSERT INTO itens (nome, categoria_id, preco, quantidade, comprado) VALUES (%s, %s, %s, 1, FALSE)" if hasattr(conn, 'info') else "INSERT INTO itens (nome, categoria_id, preco, quantidade, comprado) VALUES (?, ?, ?, 1, 0)"
    cursor.execute(query, (item.nome, item.categoria_id, item.preco))
    conn.commit()
    conn.close()
    return {"mensagem": "Item adicionado"}

@app.put("/itens/{item_id}")
def alternar_comprado(item_id: int):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE itens SET comprado = NOT comprado WHERE id = %s" if hasattr(conn, 'info') else "UPDATE itens SET comprado = NOT comprado WHERE id = ?"
    cursor.execute(query, (item_id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Status atualizado"}

@app.put("/itens/{item_id}/preco")
def atualizar_preco(item_id: int, dados: PrecoUpdate):
    conn = conectar()
    cursor = conn.cursor()
    query = "UPDATE itens SET preco = %s WHERE id = %s" if hasattr(conn, 'info') else "UPDATE itens SET preco = ? WHERE id = ?"
    cursor.execute(query, (dados.preco, item_id))
    conn.commit()
    conn.close()
    return {"mensagem": "Preço atualizado"}

@app.put("/itens/{item_id}/{acao}")
def alterar_quantidade(item_id: int, acao: str):
    conn = conectar()
    cursor = conn.cursor()
    if acao == "aumentar":
        query = "UPDATE itens SET quantidade = quantidade + 1 WHERE id = %s" if hasattr(conn, 'info') else "UPDATE itens SET quantidade = quantidade + 1 WHERE id = ?"
        cursor.execute(query, (item_id,))
    elif acao == "diminuir":
        query = "UPDATE itens SET quantidade = CASE WHEN quantidade > 1 THEN quantidade - 1 ELSE 1 END WHERE id = %s" if hasattr(conn, 'info') else "UPDATE itens SET quantidade = CASE WHEN quantidade > 1 THEN quantidade - 1 ELSE 1 END WHERE id = ?"
        cursor.execute(query, (item_id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Quantidade atualizada"}

@app.delete("/itens/{item_id}")
def deletar_item(item_id: int):
    conn = conectar()
    cursor = conn.cursor()
    query = "DELETE FROM itens WHERE id = %s" if hasattr(conn, 'info') else "DELETE FROM itens WHERE id = ?"
    cursor.execute(query, (item_id,))
    conn.commit()
    conn.close()
    return {"mensagem": "Item excluído"}

@app.delete("/itens-comprados")
def limpar_comprados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM itens WHERE comprado = TRUE" if hasattr(conn, 'info') else "DELETE FROM itens WHERE comprado = 1")
    conn.commit()
    conn.close()
    return {"mensagem": "Itens comprados removidos"}

@app.get("/produto/{codigo_barras}")
def buscar_produto(codigo_barras: str):
    # 1. Primeiro consulta na memória local do próprio app
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT nome FROM produtos_conhecidos WHERE codigo_barras = %s" if hasattr(conn, 'info') else "SELECT nome FROM produtos_conhecidos WHERE codigo_barras = ?"
    cursor.execute(query, (codigo_barras,))
    resultado_local = cursor.fetchone()
    conn.close()

    if resultado_local:
        return {"encontrado": True, "nome": resultado_local[0], "origem": "local"}

    # 2. Se não estiver na memória local, busca no Open Food Facts
    url = f"https://world.openfoodfacts.org/api/v0/product/{codigo_barras}.json"
    try:
        resposta = requests.get(url, timeout=6).json()
        if resposta.get("status") == 1:
            produto = resposta.get("product", {})
            nome = produto.get("product_name_pt") or produto.get("product_name") or ""
            marca = produto.get("brands", "")
            nome_completo = f"{nome} - {marca}".strip(" -") if marca else nome
            if nome_completo:
                return {"encontrado": True, "nome": nome_completo, "origem": "openfoodfacts"}
    except Exception:
        pass

    return {"encontrado": False, "nome": ""}