import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

from api import buscar_dados_api
from banco import (
    criar_tabela,
    salvar_instituicao,
    buscar_slug,
    listar_status,
    listar_por_inicial
)
from normalizacao import (
    gerar_slug,
    limpar_nome,
    comparar_nomes
)

console = Console()

def mostrar_titulo():
    console.print(Panel.fit(
        "Sistema de Instituições Financeiras",
        style="bold blue"
    ))

def mostrar_menu():
    console.print("\n[bold]Menu de Opções:[/bold]")
    console.print("1 - Sincronizar Instituições")
    console.print("2 - Buscar por slug")
    console.print("3 - Listar por status")
    console.print("4 - Normalizar nome")
    console.print("5 - Comparar nomes")
    console.print("6 - Exportar por inicial")
    console.print("0 - Sair")

def sincronizar():
    console.print("[yellow]Buscando dados na API... Aguarde.[/yellow]")
    dados = buscar_dados_api()
    
    if not dados:
        console.print("[red]Falha ao obter dados da API ou lista vazia.[/red]")
        return

    total = 0
    normalizados = 0

    tabela = Table(title="Primeiras 10 Instituições Sincronizadas")
    tabela.add_column("Código", style="cyan")
    tabela.add_column("Nome", style="white")
    tabela.add_column("Slug", style="yellow")
    tabela.add_column("Status", style="magenta")

    for instituicao in dados:
        dados_corretora = {
            "cnpj": instituicao.get("cnpj"),
            "codigo": instituicao.get("codigo_cvm"),
            "nome": instituicao.get("nome_social"),
            "status": instituicao.get("status"),
            "slug": gerar_slug(instituicao.get("nome_social"))
        }

        if dados_corretora["slug"] != dados_corretora["nome"].lower().replace(" ", "-"):
            normalizados += 1

        salvar_instituicao(
            dados_corretora["cnpj"],
            dados_corretora["codigo"],
            dados_corretora["nome"],
            dados_corretora["slug"],
            dados_corretora["status"]
        )

        total += 1
        
        if total <= 10:
            tabela.add_row(
                str(dados_corretora["codigo"]),
                dados_corretora["nome"],
                dados_corretora["slug"],
                dados_corretora["status"]
            )

    console.print(tabela)
    console.print(f"\n[green]Total sincronizado com sucesso:[/green] {total}")
    console.print(f"[yellow]Nomes que precisaram de normalização:[/yellow] {normalizados}")

def pesquisar_slug():
    termo = Prompt.ask("\nDigite o termo de busca para o slug").strip()
    if not termo:
        console.print("[red]O termo de busca não pode ser vazio.[/red]")
        return

    resultados = buscar_slug(termo)
    
    if not resultados:
        console.print("[red]Nenhum slug correspondente encontrado.[/red]")
        return

    tabela = Table(title=f"Resultados para: '{termo}'")
    tabela.add_column("CNPJ", style="cyan")
    tabela.add_column("Nome Original", style="white")
    tabela.add_column("Slug", style="yellow")
    tabela.add_column("Status", style="magenta")
    
    for cnpj, nome_original, slug, status in resultados:
        tabela.add_row(cnpj, nome_original, slug, status)
        
    console.print(tabela)

def pesquisar_status():
    status = Prompt.ask("\nDigite o status desejado (ex: EM FUNCIONAMENTO NORMAL)").upper().strip()
    resultados = listar_status(status)
    
    if not resultados:
        console.print("[red]Nenhuma instituição encontrada com esse status.[/red]")
        return

    tabela = Table(title=f"Instituições com Status: {status}")
    tabela.add_column("Nome Original", style="white")
    tabela.add_column("Slug", style="yellow")
    
    for nome_original, slug in resultados:
        tabela.add_row(nome_original, slug)
        
    console.print(tabela)

def normalizar_nome_usuario():
    nome_digitado = Prompt.ask("\nDigite um nome de instituição livremente").strip()
    if not nome_digitado:
        return
    
    slug_gerado = gerar_slug(nome_digitado)
    versao_limpa = limpar_nome(nome_digitado)
    
    console.print(f"\n[bold]Nome original:[/bold] {nome_digitado}")
    console.print(f"[bold yellow]Slug gerado:[/bold yellow] {slug_gerado}")
    console.print(f"[bold green]Versão limpa (sem sufixos):[/bold green] {versao_limpa}")

def comparar():
    nome1 = Prompt.ask("\nDigite o primeiro nome de instituição").strip()
    nome2 = Prompt.ask("Digite o segundo nome de instituição").strip()
    
    if not nome1 or not nome2:
        console.print("[red]Ambos os nomes devem ser preenchidos.[/red]")
        return
        
    sao_iguais = comparar_nomes(nome1, nome2)
    
    if sao_iguais:
        console.print("\n[green]Os slugs são idênticos! Refere-se à mesma instituição.[/green]")
    else:
        console.print("\n[red]Os slugs são diferentes. São instituições distintas.[/red]")

def exportar():
    letra = Prompt.ask("\nDigite uma letra do alfabeto").lower().strip()
    
    if len(letra) != 1 or not letra.isalpha():
        console.print("[red]Por favor, digite apenas uma única letra válida.[/red]")
        return
        
    resultados = listar_por_inicial(letra)
    
    if not resultados:
        console.print(f"[yellow]Nenhuma instituição inicia com a letra '{letra.upper()}'.[/yellow]")
        return
    
    tabela = Table(title=f"Slugs Iniciados com a Letra '{letra.upper()}'")
    tabela.add_column("Nome Original", style="white")
    tabela.add_column("Slug", style="yellow")
    
    for nome_original, slug in resultados:
        tabela.add_row(nome_original, slug)
        
    console.print(tabela)
    console.print(f"\n[blue]Total encontrado:[/blue] {len(resultados)}")

def main():
    criar_tabela()
    
    while True:
        mostrar_titulo()
        mostrar_menu()
        
        opcao = Prompt.ask(
            "\nEscolha uma opção", 
            choices=["0", "1", "2", "3", "4", "5", "6"],
            show_choices=False
        )

        if opcao == "1":
            sincronizar()
        elif opcao == "2":
            pesquisar_slug()
        elif opcao == "3":
            pesquisar_status()
        elif opcao == "4":
            normalizar_nome_usuario()
        elif opcao == "5":
            comparar()
        elif opcao == "6":
            exportar()
        elif opcao == "0":
            console.print("\n[bold red]Encerrando o programa... Até logo![/bold red]")
            sys.exit()

if __name__ == "__main__":
    main()
