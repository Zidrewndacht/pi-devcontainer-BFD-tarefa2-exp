from rich.console import Console
from api import buscar_feriados
from database import *
from dates import *
from display import *
from datetime import datetime


console = Console()


def iniciar():
    while True:
        console.print("\n[bold cyan]=== GESTÃO DE FERIADOS ===[/bold cyan]")
        console.print("1 - Consultar e armazenar feriados")
        console.print("2 - Verificar uma data")
        console.print("3 - Próximos feriados")
        console.print("4 - Dias úteis entre duas datas")
        console.print("5 - Listar feriados")
        console.print("0 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":

            ano = input("Informe o ano: ")

            if not ano.isdigit():
                console.print("[red]Ano inválido.[/red]")
                continue

            feriados = buscar_feriados(ano)

            if not feriados:
                console.print("[red]Nenhum dado encontrado.[/red]")
                continue

            inseridos = 0
            repetidos = 0

            for feriado in feriados:

                data = converter_data(feriado["date"])

                sucesso = inserir_feriado(
                    int(ano),
                    data.strftime("%Y-%m-%d"),
                    feriado["name"],
                    feriado["type"],
                    dia_da_semana(data)
                )

                if sucesso:
                    inseridos += 1
                else:
                    repetidos += 1

            mostrar_resumo(inseridos, repetidos)

        elif opcao == "2":

            entrada = input("Digite uma data: ")

            try:

                data = converter_data(entrada)

            except Exception:

                console.print("[red]Data inválida.[/red]")
                continue

            data_iso = data.strftime("%Y-%m-%d")

            resultado = buscar_por_data(data_iso)

            if resultado:

                diferenca = dias_diferenca(data)

                if diferenca > 0:

                    msg = f"Faltam {diferenca} dias."

                elif diferenca < 0:

                    msg = f"Passaram {-diferenca} dias."

                else:

                    msg = "É hoje!"

                mostrar_status(
                    "FERIADO",
                    f"{resultado[3]}\n{msg}",
                    "green"
                )

            elif fim_de_semana(data):

                mostrar_status(
                    "FIM DE SEMANA",
                    "A data informada cai em um sábado ou domingo.",
                    "yellow"
                )

            else:

                mostrar_status(
                    "DIA ÚTIL",
                    "A data informada não é feriado.",
                    "cyan"
                )

        elif opcao == "3":

            entrada = input(
                "Quantos próximos feriados deseja ver? "
            )

            if not entrada.isdigit():

                console.print(
                    "[red]Informe um número válido.[/red]"
                )

                continue


            quantidade = int(entrada)


            hoje = datetime.today().strftime(
                "%Y-%m-%d"
            )


            resultados = buscar_proximos(
                hoje,
                quantidade
            )


            if not resultados:

                console.print(
                    "[yellow]Nenhum feriado encontrado.[/yellow]"
                )

                continue


            lista = []


            for feriado in resultados:

                data = converter_data(
                    feriado[1]
                )


                lista.append(
                    {
                        "nome": feriado[2],
                        "data": feriado[1],
                        "dia_semana": feriado[4],
                        "dias": dias_restantes(data)
                    }
                )


            mostrar_proximos(lista)

        elif opcao == "4":

            inicio_texto = input(
                "Data inicial: "
            )

            fim_texto = input(
                "Data final: "
            )


            try:

                inicio = converter_data(inicio_texto)
                fim = converter_data(fim_texto)


            except Exception:

                console.print(
                    "[red]Datas inválidas.[/red]"
                )

                continue



            if inicio > fim:

                console.print(
                    "[red]A data inicial deve ser menor.[/red]"
                )

                continue



            inicio_iso = inicio.strftime(
                "%Y-%m-%d"
            )

            fim_iso = fim.strftime(
                "%Y-%m-%d"
            )


            feriados = buscar_feriados_periodo(
                inicio_iso,
                fim_iso
            )


            datas_feriados = set()


            for feriado in feriados:

                datas_feriados.add(
                    feriado[1]
                )


            total = 0


            for dia in gerar_intervalo(
                inicio,
                fim
            ):


                dia_iso = dia.strftime(
                    "%Y-%m-%d"
                )


                if (
                    eh_dia_util(dia)
                    and dia_iso not in datas_feriados
                ):

                    total += 1



            mostrar_dias_uteis(
                total,
                feriados
            )

        elif opcao == "5":

            filtro = input(
                "Digite um ano para filtrar ou ENTER para todos: "
            )


            if filtro == "":

                resultado = listar_feriados()


            elif filtro.isdigit():

                resultado = listar_feriados(
                    int(filtro)
                )


            else:

                console.print(
                    "[red]Ano inválido.[/red]"
                )

                continue



            if resultado:

                mostrar_lista_feriados(
                    resultado
                )

            else:

                console.print(
                    "[yellow]Nenhum feriado encontrado.[/yellow]"
                )

        elif opcao == "0":
            console.print("[green]Até logo![/green]")
            break

        else:
            console.print("[red]Opção inválida.[/red]")