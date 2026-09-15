import csv
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from models import Municipio


CAMPOS = [
    "id_ibge",
    "nome",
    "uf",
    "latitude",
    "longitude",
    "data_consulta",
    "fonte_coordenada",
    "coordenada_aproximada",
    "endereco_retornado",
]


def exportar_csv(municipios: list[Municipio], diretorio: Path) -> Path:
    caminho = diretorio / f"municipios_{datetime.now():%Y%m%d_%H%M%S}.csv"
    with caminho.open("w", newline="", encoding="utf-8-sig") as saida:
        escritor = csv.DictWriter(saida, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(asdict(municipio) for municipio in municipios)
    return caminho


def exportar_json(municipios: list[Municipio], diretorio: Path) -> Path:
    caminho = diretorio / f"municipios_{datetime.now():%Y%m%d_%H%M%S}.json"
    dados = [asdict(municipio) for municipio in municipios]
    with caminho.open("w", encoding="utf-8") as saida:
        json.dump(dados, saida, ensure_ascii=False, indent=2)
    return caminho
