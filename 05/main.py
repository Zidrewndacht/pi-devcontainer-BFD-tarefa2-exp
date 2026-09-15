from rich.console import Console

from config import carregar_configuracao
from database import BancoDados
from geocodificador import Geocodificador
from ibge_api import ClienteIBGE
from interface import InterfaceTerminal
from logging_config import configurar_logging
from servicos import ServicoMunicipios


def criar_aplicacao() -> InterfaceTerminal:
    configuracao = carregar_configuracao()
    configurar_logging(configuracao.arquivo_log)
    banco = BancoDados(configuracao.banco)
    banco.criar_estrutura()
    ibge = ClienteIBGE(configuracao.ibge_url, configuracao.timeout)
    geocodificador = Geocodificador(
        configuracao.user_agent,
        configuracao.nominatim_domain,
        configuracao.timeout,
        configuracao.intervalo_requisicoes,
    )
    servico = ServicoMunicipios(
        banco,
        ibge,
        geocodificador,
        configuracao.arquivo_capitais,
        configuracao.intervalo_requisicoes,
    )
    return InterfaceTerminal(servico, banco, configuracao)


def main() -> None:
    console = Console()
    try:
        criar_aplicacao().executar()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação interrompida pelo usuário.[/]")


if __name__ == "__main__":
    main()
