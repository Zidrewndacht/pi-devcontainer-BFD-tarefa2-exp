import sqlite3

NOME_BANCO = "corretoras.db"

def obter_conexao():
    return sqlite3.connect(NOME_BANCO)

def criar_tabela():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes (
            cnpj TEXT PRIMARY KEY,
            codigo TEXT,
            nome_original TEXT,
            slug TEXT,
            status TEXT
        )
    """)

    conexao.commit()
    conexao.close()

def salvar_instituicao(cnpj, codigo, nome_original, slug, status):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO instituicoes
        (cnpj, codigo, nome_original, slug, status)
        VALUES (?, ?, ?, ?, ?)
    """, (cnpj, codigo, nome_original, slug, status))

    conexao.commit()
    conexao.close()

def buscar_slug(slug):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT cnpj, nome_original, slug, status
        FROM instituicoes
        WHERE slug LIKE ?
    """, (f"%{slug}%",))

    resultados = cursor.fetchall()
    conexao.close()
    
    if not resultados:
        return buscar_proximos_lexicograficos(slug)

    return resultados

def buscar_proximos_lexicograficos(slug_alvo):
    """Busca os slugs mais próximos em ordem alfabética caso a busca exata falhe."""
    conexao = obter_conexao()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT cnpj, nome_original, slug, status FROM instituicoes ORDER BY slug ASC")
    todos = cursor.fetchall()
    conexao.close()
    
    if not todos:
        return []
        
    posicao = 0
    for i, linha in enumerate(todos):
        if linha[2] >= slug_alvo: 
            posicao = i
            break
            
    inicio = max(0, posicao - 1)
    fim = min(len(todos), posicao + 2)
    return todos[inicio:fim]

def listar_status(status):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome_original, slug
        FROM instituicoes
        WHERE status = ?
    """, (status,))

    resultados = cursor.fetchall()
    conexao.close()

    return resultados

def listar_por_inicial(inicial):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT nome_original, slug
        FROM instituicoes
        WHERE slug LIKE ?
    """, (f"{inicial.lower()}%",))

    resultados = cursor.fetchall()
    conexao.close()

    return resultados
