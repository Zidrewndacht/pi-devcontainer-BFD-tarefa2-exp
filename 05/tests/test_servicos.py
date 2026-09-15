import tempfile
import unittest
from pathlib import Path

from database import BancoDados
from geocodificador import (
    Geocodificador,
    LocalizacaoNaoEncontrada,
    ServicoGeocodificacaoIndisponivel,
)
from models import ResultadoGeocodificacao
from servicos import ServicoMunicipios


class IBGEFalso:
    itens = [
        {"id": 4106902, "nome": "Curitiba", "uf": "PR"},
        {"id": 4113700, "nome": "Londrina", "uf": "PR"},
    ]

    def listar_municipios(self, uf: str) -> list[dict[str, int | str]]:
        return self.itens

    def encontrar_municipio(self, nome: str, uf: str) -> dict[str, int | str] | None:
        return next(
            (
                item
                for item in self.itens
                if str(item["nome"]).casefold() == nome.casefold()
            ),
            None,
        )


class GeocodificadorFalso:
    coordenadas = {
        "Curitiba": (-25.4284, -49.2733),
        "Londrina": (-23.3045, -51.1696),
    }

    def geocodificar(self, nome: str, uf: str) -> ResultadoGeocodificacao:
        latitude, longitude = self.coordenadas[nome]
        return ResultadoGeocodificacao(latitude, longitude, f"{nome}, {uf}, Brasil")

    distancia = staticmethod(Geocodificador.distancia)


class GeocodificadorIndisponivel(GeocodificadorFalso):
    def geocodificar(self, nome: str, uf: str) -> ResultadoGeocodificacao:
        raise ServicoGeocodificacaoIndisponivel("indisponível")


class GeocodificadorSemResultado(GeocodificadorFalso):
    def geocodificar(self, nome: str, uf: str) -> ResultadoGeocodificacao:
        raise LocalizacaoNaoEncontrada("sem resultado")


class TestServicoMunicipios(unittest.TestCase):
    def setUp(self) -> None:
        self.pasta = tempfile.TemporaryDirectory()
        self.banco = BancoDados(Path(self.pasta.name) / "teste.db")
        self.banco.criar_estrutura()
        capitais = Path(__file__).resolve().parents[1] / "dados" / "capitais.json"
        self.servico = ServicoMunicipios(
            self.banco, IBGEFalso(), GeocodificadorFalso(), capitais, 1.1
        )

    def tearDown(self) -> None:
        self.pasta.cleanup()

    def test_sincronizacao_cache_e_distancia(self) -> None:
        atualizacoes = []
        primeira = self.servico.sincronizar(
            "PR", lambda atual, total, nome: atualizacoes.append((atual, total, nome))
        )
        segunda = self.servico.sincronizar(
            "PR", lambda atual, total, nome: atualizacoes.append((atual, total, nome))
        )
        terceira = self.servico.sincronizar("PR")
        self.assertEqual(primeira["sucessos"], 2)
        self.assertEqual(segunda["cache"], 2)
        self.assertEqual(terceira["cache"], 2)
        self.assertEqual(len(atualizacoes), 4)
        distancia = self.servico.calcular_distancia("Curitiba", "PR", "Londrina", "PR")
        self.assertGreater(distancia["quilometros"], 300)
        self.assertFalse(distancia["vizinhos"])
        proximos = self.servico.municipios_proximos("Curitiba", "PR", 500)
        self.assertEqual(proximos[0]["municipio"].nome, "Londrina")
        self.assertEqual(self.servico.municipios_proximos("Curitiba", "PR", 10), [])
        estatisticas = self.banco.estatisticas()
        self.assertIsNotNone(estatisticas["ultima_sincronizacao"])

        distancia_original = self.servico.geocodificador.distancia
        self.servico.geocodificador.distancia = lambda origem, destino: (10.0, 6.2)
        try:
            vizinhos = self.servico.calcular_distancia(
                "Curitiba", "PR", "Londrina", "PR"
            )
        finally:
            self.servico.geocodificador.distancia = distancia_original
        self.assertTrue(vizinhos["vizinhos"])

    def test_municipio_inexistente_no_ibge(self) -> None:
        with self.assertRaises(Exception) as erro:
            self.servico.obter_municipio("Cidade inventada", "PR")
        self.assertIn("não consta", str(erro.exception))

    def test_fallback_da_capital(self) -> None:
        capitais = Path(__file__).resolve().parents[1] / "dados" / "capitais.json"
        servico = ServicoMunicipios(
            self.banco, IBGEFalso(), GeocodificadorIndisponivel(), capitais, 1.1
        )
        with self.assertLogs(level="WARNING"):
            resultado = servico.sincronizar("PR")
        curitiba = self.banco.buscar_municipio("Curitiba", "PR")
        self.assertEqual(resultado["aproximados"], 2)
        self.assertTrue(curitiba.coordenada_aproximada)
        self.assertEqual(curitiba.fonte_coordenada, "capital_fallback")

    def test_fallback_em_busca_direta(self) -> None:
        capitais = Path(__file__).resolve().parents[1] / "dados" / "capitais.json"
        servico = ServicoMunicipios(
            self.banco, IBGEFalso(), GeocodificadorIndisponivel(), capitais, 1.1
        )
        with self.assertLogs(level="WARNING"):
            curitiba = servico.obter_municipio("Curitiba", "PR")
        self.assertTrue(curitiba.coordenada_aproximada)

    def test_sincronizacao_sem_resultados_do_geocodificador(self) -> None:
        capitais = Path(__file__).resolve().parents[1] / "dados" / "capitais.json"
        servico = ServicoMunicipios(
            self.banco, IBGEFalso(), GeocodificadorSemResultado(), capitais, 1.1
        )
        with self.assertLogs(level="WARNING"):
            resultado = servico.sincronizar("PR")
        self.assertEqual(resultado["falhas"], 2)
        self.assertEqual(self.banco.listar_municipios(), [])


if __name__ == "__main__":
    unittest.main()
