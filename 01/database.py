import sqlite3

BANCO = "feriados.db"


def conectar():
    return sqlite3.connect(BANCO)


def listar_feriados(ano=None):

    conn = conectar()
    cursor = conn.cursor()


    if ano:

        cursor.execute("""
            SELECT ano, data, nome, tipo, dia_semana
            FROM feriados
            WHERE ano = ?
            ORDER BY data
        """, (ano,))


    else:

        cursor.execute("""
            SELECT ano, data, nome, tipo, dia_semana
            FROM feriados
            ORDER BY data
        """)


    dados = cursor.fetchall()

    conn.close()


    return dados


def buscar_feriados_periodo(inicio, fim):

    conn = conectar()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        WHERE data BETWEEN ? AND ?
        ORDER BY data
    """, (inicio, fim))


    dados = cursor.fetchall()

    conn.close()


    return dados


def buscar_proximos(data, limite):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        WHERE data >= ?
        ORDER BY data
        LIMIT ?
    """, (data, limite))

    dados = cursor.fetchall()

    conn.close()

    return dados


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feriados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ano INTEGER NOT NULL,
            data TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            dia_semana TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def inserir_feriado(ano, data, nome, tipo, dia_semana):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO feriados
            (ano, data, nome, tipo, dia_semana)
            VALUES (?, ?, ?, ?, ?)
        """, (ano, data, nome, tipo, dia_semana))

        conn.commit()
        inserido = True

    except sqlite3.IntegrityError:
        inserido = False

    conn.close()

    return inserido

def buscar_por_data(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM feriados
        WHERE data = ?
    """, (data,))

    resultado = cursor.fetchone()

    conn.close()

    return resultado

def listar_todos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        ORDER BY data
    """)

    dados = cursor.fetchall()

    conn.close()

    return dados

def listar_por_ano(ano):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        WHERE ano = ?
        ORDER BY data
    """, (ano,))

    dados = cursor.fetchall()

    conn.close()

    return dados

def proximos_feriados(data):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        WHERE data >= ?
        ORDER BY data
    """, (data,))

    dados = cursor.fetchall()

    conn.close()

    return dados

def feriados_no_periodo(inicio, fim):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ano, data, nome, tipo, dia_semana
        FROM feriados
        WHERE data BETWEEN ? AND ?
        ORDER BY data
    """, (inicio, fim))

    dados = cursor.fetchall()

    conn.close()

    return dados