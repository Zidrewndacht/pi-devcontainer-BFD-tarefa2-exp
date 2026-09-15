import sqlite3

def conectar():
    conn = sqlite3.connect('banco.db')
    conn.execute("CREATE TABLE IF NOT EXISTS fipe_cache (id INTEGER PRIMARY KEY, codigo_fipe TEXT, marca TEXT, modelo TEXT, ano_modelo INTEGER, preco REAL, preco_extenso TEXT)")
    return conn

def buscar_por_fipe(codigo_fipe):
    conn = conectar()
    res = conn.execute("SELECT * FROM fipe_cache WHERE codigo_fipe = ? LIMIT 1", (codigo_fipe,)).fetchone()
    conn.close()
    return res

def salvar_consulta(dados):
    conn = conectar()
    conn.execute("INSERT INTO fipe_cache (codigo_fipe, marca, modelo, ano_modelo, preco, preco_extenso) VALUES (?,?,?,?,?,?)", dados)
    conn.commit()
    conn.close()

def is_no_banco(codigo_fipe):
    conn = conectar()
    res = conn.execute("SELECT * FROM fipe_cache WHERE codigo_fipe = ? LIMIT 1", (codigo_fipe,)).fetchone()
    if res == None:
        conn.close()
        return False
    else:
        conn.close()
        return True

