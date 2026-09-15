from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def montar_dashboard(estatisticas: dict[str, object]) -> Layout:
    layout = Layout()
    layout.split_column(Layout(name="cabecalho", size=3), Layout(name="corpo"))
    layout["corpo"].split_row(Layout(name="resumo"), Layout(name="detalhes"))
    layout["cabecalho"].update(
        Panel(
            Align.center("PAINEL DE ESTATÍSTICAS", vertical="middle"), style="bold cyan"
        )
    )
    resumo = Table.grid(padding=(0, 1))
    resumo.add_column(style="bold")
    resumo.add_column(justify="right")
    resumo.add_row("Municípios", str(estatisticas["total"]))
    resumo.add_row("UFs", str(estatisticas["ufs"]))
    resumo.add_row("Aproximados", str(estatisticas["aproximados"]))
    resumo.add_row("Última consulta", str(estatisticas["ultima_consulta"] or "Nenhuma"))
    distribuicao = Table(title="Distribuição por UF", expand=True)
    distribuicao.add_column("UF", style="cyan")
    distribuicao.add_column("Quantidade", justify="right")
    for item in estatisticas["distribuicao"]:
        distribuicao.add_row(str(item["uf"]), str(item["quantidade"]))
    fontes = Table(title="Origem das coordenadas", expand=True)
    fontes.add_column("Fonte", style="magenta")
    fontes.add_column("Quantidade", justify="right")
    for item in estatisticas["fontes"]:
        fontes.add_row(str(item["fonte_coordenada"]), str(item["quantidade"]))
    layout["resumo"].update(Panel(resumo, title="Resumo", border_style="green"))
    layout["detalhes"].update(
        Panel(Group(distribuicao, Text(""), fontes), border_style="blue")
    )
    return layout
