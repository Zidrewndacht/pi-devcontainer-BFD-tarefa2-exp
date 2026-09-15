import logging
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.prompt import Confirm, Prompt
from rich.table import Table

from batch import processar_arquivo
from config import Configuracao
from dashboard import montar_dashboard
from database import BancoDados
from exportacao import exportar_csv, exportar_json
from mapa_ascii import gerar_mapa
from models import Municipio
from servicos import ServicoMunicipios
from validacoes import validar_raio, validar_uf


class InterfaceTerminal:
    def __init__(
        self,
        servico: ServicoMunicipios,
        banco: BancoDados,
        configuracao: Configuracao,
        console: Console | None = None,
    ):
        self.servico = servico
        self.banco = banco
        self.configuracao = configuracao
        self.console = console or Console()

    def executar(self) -> None:
        opcoes = {
            "1": self.sincronizar,
            "2": self.buscar,
            "3": self.calcular_distancia,
            "4": self.listar_proximos,
            "5": self.listar_sincronizados,
            "6": self.mapa_ascii,
            "7": self.exportar,
            "8": self.processar_batch,
            "9": self.dashboard,
            "10": self.exibir_configuracoes,
        }
        while True:
            self._cabecalho()
            escolha = Prompt.ask(
                "[bold cyan]Escolha uma opção[/]", choices=[*opcoes, "0"]
            )
            logging.info("Opção de menu selecionada: %s", escolha)
            if escolha == "0":
                self.console.print(Panel("Aplicação encerrada.", border_style="cyan"))
                return
            try:
                opcoes[escolha]()
            except (ValueError, RuntimeError, FileNotFoundError) as erro:
                logging.exception("Erro na opção %s", escolha)
                self.console.print(
                    Panel(
                        str(erro), title="Não foi possível concluir", border_style="red"
                    )
                )
            self.console.print()
            Prompt.ask(
                "Pressione [bold]Enter[/] para voltar ao menu",
                default="",
                show_default=False,
            )

    def sincronizar(self) -> None:
        uf = self._pedir_uf()
        self.console.print(
            Panel(
                "A sincronização respeita o intervalo do Nominatim e pode levar alguns minutos. "
                "Registros já armazenados são carregados do cache.",
                title=f"Sincronização de {uf}",
                border_style="yellow",
            )
        )
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
            console=self.console,
        ) as progresso:
            tarefa = progresso.add_task("Consultando IBGE...", total=1)

            def atualizar(atual: int, total: int, nome: str) -> None:
                progresso.update(tarefa, completed=atual, total=total, description=nome)

            resultado = self.servico.sincronizar(uf, atualizar)
        medias = resultado["medias"]
        media_texto = "Sem coordenadas"
        if medias:
            media_texto = f"{medias[0]:.6f} / {medias[1]:.6f}"
        tabela = Table.grid(padding=(0, 2))
        tabela.add_column(style="bold")
        tabela.add_column(justify="right")
        tabela.add_row("Municípios da UF", str(resultado["total"]))
        tabela.add_row("Geocodificados agora", str(resultado["sucessos"]))
        tabela.add_row("Obtidos do cache", str(resultado["cache"]))
        tabela.add_row("Coordenadas aproximadas", str(resultado["aproximados"]))
        tabela.add_row("Falhas", str(resultado["falhas"]))
        tabela.add_row("Média latitude / longitude", media_texto)
        tabela.add_row(
            "Estimativa inicial",
            self._formatar_tempo(float(resultado["estimativa_segundos"])),
        )
        tabela.add_row(
            "Tempo decorrido",
            self._formatar_tempo(float(resultado["duracao_segundos"])),
        )
        self.console.print(
            Panel(tabela, title="Resumo da sincronização", border_style="green")
        )

    def buscar(self) -> None:
        nome, uf = self._pedir_municipio()
        municipio = self.servico.obter_municipio(nome, uf)
        self._exibir_municipio(municipio)

    def calcular_distancia(self) -> None:
        self.console.print("[bold]Município de origem[/]")
        nome_origem, uf_origem = self._pedir_municipio()
        self.console.print("[bold]Município de destino[/]")
        nome_destino, uf_destino = self._pedir_municipio()
        resultado = self.servico.calcular_distancia(
            nome_origem, uf_origem, nome_destino, uf_destino
        )
        classificacao = "Vizinhos" if resultado["vizinhos"] else "Não são vizinhos"
        aviso = (
            "\n[yellow]Resultado baseado em pelo menos uma coordenada aproximada.[/]"
            if resultado["aproximada"]
            else ""
        )
        texto = (
            f"[bold]{resultado['origem'].nome}/{resultado['origem'].uf}[/] -> "
            f"[bold]{resultado['destino'].nome}/{resultado['destino'].uf}[/]\n\n"
            f"[cyan]{resultado['quilometros']:.2f} km[/]\n"
            f"[magenta]{resultado['milhas']:.2f} milhas[/]\n"
            f"[green]{classificacao}[/]{aviso}"
        )
        self.console.print(
            Panel(texto, title="Distância geodésica", border_style="blue")
        )

    def listar_proximos(self) -> None:
        nome, uf = self._pedir_municipio()
        raio = validar_raio(Prompt.ask("Raio em quilômetros"))
        encontrados = self.servico.municipios_proximos(nome, uf, raio)
        tabela = Table(title=f"Municípios em um raio de {raio:.2f} km")
        tabela.add_column("Município", style="bold")
        tabela.add_column("UF", justify="center")
        tabela.add_column("Distância", justify="right", style="cyan")
        tabela.add_column("Coordenada", justify="center")
        for item in encontrados:
            municipio = item["municipio"]
            tabela.add_row(
                municipio.nome,
                municipio.uf,
                f"{item['distancia']:.2f} km",
                "aproximada" if municipio.coordenada_aproximada else "real",
            )
        if encontrados:
            self.console.print(tabela)
        else:
            self.console.print(
                Panel(
                    "Nenhum município sincronizado foi encontrado nesse raio.",
                    border_style="yellow",
                )
            )

    def listar_sincronizados(self) -> None:
        filtrar = Confirm.ask("Filtrar por UF?", default=False)
        uf = self._pedir_uf() if filtrar else None
        municipios = self.banco.listar_municipios(uf)
        self._exibir_tabela_municipios(municipios, "Municípios sincronizados")

    def mapa_ascii(self) -> None:
        uf = self._pedir_uf()
        municipios = self.banco.listar_municipios(uf)
        mapa = gerar_mapa(municipios)
        self.console.print(Panel(mapa, title=f"Mapa ASCII — {uf}", border_style="cyan"))

    def exportar(self) -> None:
        formato = Prompt.ask("Formato", choices=["csv", "json"], default="csv")
        filtrar = Confirm.ask("Exportar apenas uma UF?", default=False)
        uf = self._pedir_uf() if filtrar else None
        municipios = self.banco.listar_municipios(uf)
        if not municipios:
            raise ValueError("Não há registros para exportar.")
        if formato == "csv":
            caminho = exportar_csv(municipios, self.configuracao.diretorio_exportacao)
        else:
            caminho = exportar_json(municipios, self.configuracao.diretorio_exportacao)
        logging.info("Exportação criada em %s", caminho)
        self.console.print(
            Panel(
                f"{len(municipios)} registros exportados para:\n{caminho}",
                border_style="green",
            )
        )

    def processar_batch(self) -> None:
        padrao = str(Path("dados") / "exemplo_batch.txt")
        caminho = Path(Prompt.ask("Caminho do arquivo", default=padrao)).expanduser()
        resultado = processar_arquivo(caminho, self.servico)
        tabela = Table(title="Resultado do processamento em lote")
        tabela.add_column("Linha", justify="right")
        tabela.add_column("Entrada")
        tabela.add_column("Resultado")
        for municipio in resultado["sucessos"]:
            tabela.add_row(
                "-", f"{municipio.nome};{municipio.uf}", "sucesso", style="green"
            )
        for falha in resultado["falhas"]:
            tabela.add_row(
                str(falha["linha"]),
                str(falha["entrada"]),
                str(falha["erro"]),
                style="red",
            )
        self.console.print(tabela)
        self.console.print(
            Panel(
                f"Total: {resultado['total']} | Sucessos: {len(resultado['sucessos'])} | "
                f"Falhas: {len(resultado['falhas'])}",
                border_style="blue",
            )
        )

    def dashboard(self) -> None:
        self.console.print(montar_dashboard(self.banco.estatisticas()))

    def exibir_configuracoes(self) -> None:
        tabela = Table(title="Configurações em uso")
        tabela.add_column("Configuração", style="bold cyan")
        tabela.add_column("Valor")
        for nome in self.configuracao.__dataclass_fields__:
            tabela.add_row(nome, str(getattr(self.configuracao, nome)))
        self.console.print(tabela)

    def _cabecalho(self) -> None:
        menu = (
            "[bold cyan]1.[/] Sincronizar municípios de uma UF\n"
            "[bold cyan]2.[/] Buscar coordenadas de município\n"
            "[bold cyan]3.[/] Calcular distância entre municípios\n"
            "[bold cyan]4.[/] Municípios próximos\n"
            "[bold cyan]5.[/] Listar municípios sincronizados\n"
            "[bold cyan]6.[/] Mapa ASCII\n"
            "[bold cyan]7.[/] Exportar CSV ou JSON\n"
            "[bold cyan]8.[/] Processar arquivo em lote\n"
            "[bold cyan]9.[/] Painel de estatísticas\n"
            "[bold cyan]10.[/] Exibir configurações\n"
            "[bold red]0.[/] Sair"
        )
        self.console.print(
            Panel(
                menu,
                title="GeoAtlas Brasil - Municípios Brasileiros",
                border_style="cyan",
            )
        )

    def _pedir_uf(self) -> str:
        padrao = self.configuracao.uf_padrao or None
        return validar_uf(Prompt.ask("UF", default=padrao, show_default=bool(padrao)))

    def _pedir_municipio(self) -> tuple[str, str]:
        nome = Prompt.ask("Município").strip()
        uf = self._pedir_uf()
        return nome, uf

    def _exibir_municipio(self, municipio: Municipio) -> None:
        mapa = f"https://www.openstreetmap.org/?mlat={municipio.latitude}&mlon={municipio.longitude}#map=12/{municipio.latitude}/{municipio.longitude}"
        aproximada = "Sim" if municipio.coordenada_aproximada else "Não"
        tabela = Table.grid(padding=(0, 2))
        tabela.add_column(style="bold")
        tabela.add_column()
        tabela.add_row("Município", f"{municipio.nome}/{municipio.uf}")
        tabela.add_row("ID IBGE", str(municipio.id_ibge))
        tabela.add_row("Latitude", f"{municipio.latitude:.6f}")
        tabela.add_row("Longitude", f"{municipio.longitude:.6f}")
        tabela.add_row("Fonte", municipio.fonte_coordenada)
        tabela.add_row("Aproximada", aproximada)
        tabela.add_row("Consultado em", municipio.data_consulta)
        tabela.add_row("Mapa", f"[link={mapa}]{mapa}[/link]")
        self.console.print(Panel(tabela, title="Coordenadas", border_style="green"))

    def _exibir_tabela_municipios(
        self, municipios: list[Municipio], titulo: str
    ) -> None:
        if not municipios:
            self.console.print(
                Panel("Nenhum município sincronizado.", border_style="yellow")
            )
            return
        tabela = Table(title=titulo, show_lines=False)
        tabela.add_column("ID IBGE", justify="right")
        tabela.add_column("Município", style="bold")
        tabela.add_column("UF", justify="center")
        tabela.add_column("Latitude", justify="right")
        tabela.add_column("Longitude", justify="right")
        tabela.add_column("Fonte")
        for municipio in municipios:
            tabela.add_row(
                str(municipio.id_ibge),
                municipio.nome,
                municipio.uf,
                f"{municipio.latitude:.6f}",
                f"{municipio.longitude:.6f}",
                municipio.fonte_coordenada,
            )
        self.console.print(tabela)

    @staticmethod
    def _formatar_tempo(segundos: float) -> str:
        minutos, segundos_restantes = divmod(round(segundos), 60)
        horas, minutos_restantes = divmod(minutos, 60)
        partes = []
        if horas:
            partes.append(f"{horas} h")
        if minutos_restantes:
            partes.append(f"{minutos_restantes} min")
        partes.append(f"{segundos_restantes} s")
        return " ".join(partes)
