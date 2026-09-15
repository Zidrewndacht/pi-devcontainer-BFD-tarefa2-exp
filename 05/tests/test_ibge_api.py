import unittest
from unittest.mock import Mock, patch

import requests

from ibge_api import ClienteIBGE, ErroIBGE


class TestClienteIBGE(unittest.TestCase):
    def setUp(self) -> None:
        self.cliente = ClienteIBGE("https://exemplo.test/{uf}", 5)

    @patch("ibge_api.requests.get")
    def test_converte_resposta_em_dicionarios(self, get: Mock) -> None:
        resposta = Mock()
        resposta.json.return_value = [
            {"id": 1, "nome": "Curitiba"},
            {"id": 2, "nome": "Londrina"},
        ]
        get.return_value = resposta
        resultado = self.cliente.listar_municipios("PR")
        get.assert_called_once_with("https://exemplo.test/PR", timeout=5)
        self.assertEqual(resultado[0], {"id": 1, "nome": "Curitiba", "uf": "PR"})

    @patch("ibge_api.requests.get")
    def test_trata_falha_http(self, get: Mock) -> None:
        get.side_effect = requests.Timeout("tempo esgotado")
        with self.assertLogs(level="ERROR"):
            with self.assertRaises(ErroIBGE):
                self.cliente.listar_municipios("PR")

    @patch("ibge_api.requests.get")
    def test_rejeita_resposta_invalida_ou_vazia(self, get: Mock) -> None:
        resposta = Mock()
        get.return_value = resposta
        resposta.json.return_value = {"erro": "formato inesperado"}
        with self.assertRaises(ErroIBGE):
            self.cliente.listar_municipios("PR")
        resposta.json.return_value = [{"campo": "sem id e nome"}]
        with self.assertRaises(ErroIBGE):
            self.cliente.listar_municipios("PR")

    @patch("ibge_api.requests.get")
    def test_encontra_municipio_sem_diferenciar_acentos(self, get: Mock) -> None:
        resposta = Mock()
        resposta.json.return_value = [{"id": 1, "nome": "São José"}]
        get.return_value = resposta
        encontrado = self.cliente.encontrar_municipio("sao jose", "PR")
        self.assertEqual(encontrado["id"], 1)
        self.assertIsNone(self.cliente.encontrar_municipio("Curitiba", "PR"))


if __name__ == "__main__":
    unittest.main()
