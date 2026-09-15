import sys
import sqlite3
import requests
from slugify import slugify
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

NOME_BANCO = "corretoras.db"
API_URL = "https://brasilapi.com.br/api/cvm/corretoras/v1"

def mostrar_titulo():
    console.print(Panel("Sistema de Instituições Financeiras"))

def mostrar_menu():
    console.print("1 - Sincronizar Instituições")
    console.print("2 - Buscar por slug")
    console.print("3 - listar por status")
    console.print("0 - Sair")

def buscar_dados_api():
    resposta = requests.get(API_URL)
    return resposta.json()

def sincronizar_instituicoes():
    criar_tabela()

    dados = buscar_dados_api()

    for instituicao in dados:

        cnpj = instituicao["cnpj"]
        nome = instituicao["nome_social"]
        status = instituicao["status"]

        slug = slugify(nome)

        salvar_instituicao(
            cnpj,
            nome,
            slug,
            status
        )

    console.print("[green]Instituições sincronizadas com sucesso![/green]")
        
def buscar_slug():

    slug = input("Digite um slug: ")

    resultados = buscar_slug_banco(slug)

    if not resultados:
        console.print("[red]Nenhuma instituição encontrada.[/red]")
        return

    tabela = Table(title="Resultado da Busca")

    tabela.add_column("CNPJ", style="cyan")
    tabela.add_column("Nome", style="green")
    tabela.add_column("Slug", style="yellow")
    tabela.add_column("Status", style="magenta")

    for linha in resultados:
        tabela.add_row(linha[0], linha[1], linha[2], linha[3])

    console.print(tabela)


def listar_status():

    status = input("Digite o status (ATIVA, EM FUNCIONAMENTO NORMAL, CANCELADA): ").upper()

    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT cnpj, nome_original, slug, status
        FROM instituicoes
        WHERE status = ?
    """, (status,))

    resultados = cursor.fetchall()

    conexao.close()

    if not resultados:
        console.print("[red]Nenhuma instituição encontrada.[/red]")
        return

    tabela = Table(title=f"Instituições - {status}")

    tabela.add_column("CNPJ", style="cyan")
    tabela.add_column("Nome", style="green")
    tabela.add_column("Slug", style="yellow")
    tabela.add_column("Status", style="magenta")

    for linha in resultados:
        tabela.add_row(
            linha[0],
            linha[1],
            linha[2],
            linha[3]
        )

    console.print(tabela)


def main():
    mostrar_titulo()
    mostrar_menu()

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        sincronizar_instituicoes()

    elif opcao == "2":
        buscar_slug()

    elif opcao == "3":
        listar_status()

    elif opcao == "0":
        console.print("Encerrando o programa...")
        sys.exit()

    else:
        console.print("Opção inválida!")

def obter_conexao():
    return sqlite3.connect(NOME_BANCO)

def criar_tabela():
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS instituicoes (
            cnpj TEXT PRIMARY KEY,
            nome_original TEXT,
            slug TEXT,
            status TEXT
        )
    """)

    conexao.commit()
    conexao.close()

def salvar_instituicao(cnpj, nome_original, slug, status):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO instituicoes
        (cnpj, nome_original, slug, status)
        VALUES (?, ?, ?, ?)
    """, (cnpj, nome_original, slug, status))

    conexao.commit()
    conexao.close()

def buscar_slug_banco(slug):
    conexao = obter_conexao()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT cnpj, nome_original, slug, status
        FROM instituicoes
        WHERE slug LIKE ?
    """, (f"%{slug}%",))
    
    resultado = cursor.fetchall()

    conexao.commit()
    conexao.close()

    return resultado

if __name__ == "__main__":
    main()


