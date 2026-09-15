from rich.console import Console
from rich.table import Table

console = Console()

def mostrar_lista_feriados(feriados):

    tabela = Table(
        title="Feriados Armazenados"
    )


    tabela.add_column(
        "Ano",
        style="cyan"
    )

    tabela.add_column(
        "Data",
        style="green"
    )

    tabela.add_column(
        "Nome",
        style="yellow"
    )

    tabela.add_column(
        "Tipo"
    )

    tabela.add_column(
        "Dia da Semana"
    )


    for feriado in feriados:

        tabela.add_row(
            str(feriado[0]),
            feriado[1],
            feriado[2],
            feriado[3],
            feriado[4]
        )


    console.print(tabela)


def mostrar_dias_uteis(total, feriados):

    console.print(
        f"\n[bold green]Dias úteis encontrados: {total}[/bold green]"
    )


    if feriados:

        tabela = Table(
            title="Feriados no período"
        )


        tabela.add_column(
            "Data",
            style="cyan"
        )

        tabela.add_column(
            "Nome",
            style="yellow"
        )


        for feriado in feriados:

            tabela.add_row(
                feriado[1],
                feriado[2]
            )


        console.print(tabela)

    else:

        console.print(
            "[cyan]Nenhum feriado no período.[/cyan]"
        )


def mostrar_resumo(inseridos, repetidos):
    tabela = Table(title="Resumo da Importação")

    tabela.add_column("Inseridos", justify="center", style="green")
    tabela.add_column("Já Existiam", justify="center", style="yellow")

    tabela.add_row(str(inseridos), str(repetidos))

    console.print(tabela)

def mostrar_status(titulo, mensagem, cor="cyan"):
    console.print(f"\n[{cor}]{titulo}[/{cor}]")
    console.print(mensagem)

def mostrar_proximos(feriados):

    tabela = Table(
        title="Próximos Feriados"
    )

    tabela.add_column(
        "Nome",
        style="green"
    )

    tabela.add_column(
        "Data",
        style="cyan"
    )

    tabela.add_column(
        "Dia da Semana",
        style="yellow"
    )

    tabela.add_column(
        "Dias Restantes",
        justify="center"
    )


    for feriado in feriados:

        tabela.add_row(
            feriado["nome"],
            feriado["data"],
            feriado["dia_semana"],
            str(feriado["dias"])
        )


    console.print(tabela)