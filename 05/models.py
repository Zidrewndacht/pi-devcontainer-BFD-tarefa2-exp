from dataclasses import dataclass


@dataclass(slots=True)
class Municipio:
    id_ibge: int
    nome: str
    uf: str
    latitude: float
    longitude: float
    data_consulta: str
    fonte_coordenada: str = "nominatim"
    coordenada_aproximada: bool = False
    endereco_retornado: str = ""


@dataclass(slots=True)
class ResultadoGeocodificacao:
    latitude: float
    longitude: float
    endereco: str
