import logging

from geopy.distance import geodesic
from geopy.exc import (
    GeocoderQuotaExceeded,
    GeocoderRateLimited,
    GeocoderServiceError,
    GeocoderTimedOut,
    GeocoderUnavailable,
)
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

from models import Municipio, ResultadoGeocodificacao
from validacoes import UFS


class LocalizacaoNaoEncontrada(RuntimeError):
    pass


class ServicoGeocodificacaoIndisponivel(RuntimeError):
    pass


class LimiteGeocodificacao(ServicoGeocodificacaoIndisponivel):
    pass


class Geocodificador:
    def __init__(
        self,
        user_agent: str,
        domain: str,
        timeout: int,
        intervalo: float,
    ):
        cliente = Nominatim(user_agent=user_agent, domain=domain, timeout=timeout)
        self._consultar = RateLimiter(
            cliente.geocode,
            min_delay_seconds=intervalo,
            max_retries=2,
            error_wait_seconds=max(5.0, intervalo),
            swallow_exceptions=False,
        )

    def geocodificar(self, nome: str, uf: str) -> ResultadoGeocodificacao:
        consulta = f"{nome}, {UFS[uf]}, Brasil"
        logging.info("Geocodificação de %s/%s", nome, uf)
        try:
            local = self._consultar(
                consulta,
                exactly_one=True,
                addressdetails=True,
                language="pt-BR",
                country_codes="br",
            )
        except (GeocoderRateLimited, GeocoderQuotaExceeded) as erro:
            logging.warning("Limite do geocodificador para %s/%s", nome, uf)
            raise LimiteGeocodificacao(
                "O geocodificador atingiu o limite de requisições."
            ) from erro
        except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError) as erro:
            logging.warning(
                "Geocodificador indisponível para %s/%s: %s", nome, uf, erro
            )
            raise ServicoGeocodificacaoIndisponivel(
                "O serviço de geocodificação está indisponível."
            ) from erro
        if local is None:
            raise LocalizacaoNaoEncontrada(
                f"Não foram encontradas coordenadas para {nome}/{uf}."
            )
        return ResultadoGeocodificacao(
            latitude=float(local.latitude),
            longitude=float(local.longitude),
            endereco=str(local.address or consulta),
        )

    @staticmethod
    def distancia(origem: Municipio, destino: Municipio) -> tuple[float, float]:
        resultado = geodesic(
            (origem.latitude, origem.longitude),
            (destino.latitude, destino.longitude),
        )
        return resultado.kilometers, resultado.miles
