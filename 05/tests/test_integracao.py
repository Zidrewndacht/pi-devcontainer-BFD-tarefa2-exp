import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from rich.console import Console

from config import Configuracao
from database import BancoDados
from ibge_api import ClienteIBGE
from interface import InterfaceTerminal
from models import ResultadoGeocodificacao
from servicos import ServicoMunicipios


class GeocodificadorSimulado:
    def geocodificar(self, nome: str, uf: str) -> ResultadoGeocodificacao:
        return ResultadoGeocodificacao(-25.4284, -49.2733, "Curitiba, Paraná, Brasil")


class TestIntegracaoSimulada(unittest.TestCase):
    @patch("ibge_api.requests.get")
    def test_fluxo_api_banco_e_exibicao(self, get: Mock) -> None:
        resposta = Mock()
        resposta.json.return_value = [{"id": 4106902, "nome": "Curitiba"}]
        get.return_value = resposta
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            banco = BancoDados(raiz / "teste.db")
            banco.criar_estrutura()
            capitais = Path(__file__).resolve().parents[1] / "dados" / "capitais.json"
            ibge = ClienteIBGE("https://exemplo.test/{uf}", 5)
            servico = ServicoMunicipios(
                banco, ibge, GeocodificadorSimulado(), capitais, 1.1
            )
            resultado = servico.sincronizar("PR")
            configuracao = Configuracao(
                ibge_url="https://exemplo.test/{uf}",
                nominatim_domain="exemplo.test",
                user_agent="teste",
                timeout=5,
                intervalo_requisicoes=1.1,
                uf_padrao="PR",
                banco=raiz / "teste.db",
                arquivo_capitais=capitais,
                diretorio_exportacao=raiz,
                arquivo_log=raiz / "teste.log",
            )
            console = Console(record=True, width=120, file=io.StringIO())
            interface = InterfaceTerminal(servico, banco, configuracao, console)
            interface._exibir_tabela_municipios(banco.listar_municipios(), "Teste")
            texto = console.export_text()
            self.assertEqual(resultado["sucessos"], 1)
            self.assertIn("Curitiba", texto)
            self.assertIn("4106902", texto)


if __name__ == "__main__":
    unittest.main()
