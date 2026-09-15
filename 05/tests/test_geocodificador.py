import unittest
from types import SimpleNamespace
from unittest.mock import patch

from geopy.exc import GeocoderRateLimited, GeocoderTimedOut

from geocodificador import (
    Geocodificador,
    LimiteGeocodificacao,
    LocalizacaoNaoEncontrada,
    ServicoGeocodificacaoIndisponivel,
)


class TestGeocodificador(unittest.TestCase):
    def criar(
        self, retorno: object = None, erro: Exception | None = None
    ) -> Geocodificador:
        with (
            patch("geocodificador.Nominatim") as nominatim,
            patch("geocodificador.RateLimiter", side_effect=lambda func, **_: func),
        ):
            if erro:
                nominatim.return_value.geocode.side_effect = erro
            else:
                nominatim.return_value.geocode.return_value = retorno
            return Geocodificador("teste", "exemplo.test", 5, 1.1)

    def test_geocodificacao_com_sucesso(self) -> None:
        local = SimpleNamespace(
            latitude=-25.4284,
            longitude=-49.2733,
            address="Curitiba, Paraná, Brasil",
        )
        resultado = self.criar(local).geocodificar("Curitiba", "PR")
        self.assertAlmostEqual(resultado.latitude, -25.4284)
        self.assertIn("Curitiba", resultado.endereco)

    def test_localizacao_nao_encontrada(self) -> None:
        with self.assertRaises(LocalizacaoNaoEncontrada):
            self.criar().geocodificar("Município inexistente", "PR")

    def test_limite_e_indisponibilidade(self) -> None:
        with self.assertLogs(level="WARNING"):
            with self.assertRaises(LimiteGeocodificacao):
                self.criar(erro=GeocoderRateLimited("limite")).geocodificar(
                    "Curitiba", "PR"
                )
            with self.assertRaises(ServicoGeocodificacaoIndisponivel):
                self.criar(erro=GeocoderTimedOut("tempo esgotado")).geocodificar(
                    "Curitiba", "PR"
                )


if __name__ == "__main__":
    unittest.main()
