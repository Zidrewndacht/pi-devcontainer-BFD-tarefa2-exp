import json
import os
from dataclasses import dataclass
from pathlib import Path


RAIZ = Path(__file__).resolve().parent


@dataclass(frozen=True, slots=True)
class Configuracao:
    ibge_url: str
    nominatim_domain: str
    user_agent: str
    timeout: int
    intervalo_requisicoes: float
    uf_padrao: str
    banco: Path
    arquivo_capitais: Path
    diretorio_exportacao: Path
    arquivo_log: Path


def _caminho(valor: str) -> Path:
    caminho = Path(valor)
    return caminho if caminho.is_absolute() else RAIZ / caminho


def carregar_configuracao(arquivo: Path | None = None) -> Configuracao:
    caminho = arquivo or RAIZ / "config.json"
    with caminho.open(encoding="utf-8") as entrada:
        dados: dict[str, object] = json.load(entrada)

    def valor(nome: str) -> str:
        variavel = f"TAREFA5_{nome.upper()}"
        return os.getenv(variavel, str(dados[nome]))

    configuracao = Configuracao(
        ibge_url=valor("ibge_url"),
        nominatim_domain=valor("nominatim_domain"),
        user_agent=valor("user_agent"),
        timeout=int(valor("timeout")),
        intervalo_requisicoes=float(valor("intervalo_requisicoes")),
        uf_padrao=valor("uf_padrao").upper(),
        banco=_caminho(valor("banco")),
        arquivo_capitais=_caminho(valor("arquivo_capitais")),
        diretorio_exportacao=_caminho(valor("diretorio_exportacao")),
        arquivo_log=_caminho(valor("arquivo_log")),
    )
    configuracao.banco.parent.mkdir(parents=True, exist_ok=True)
    configuracao.diretorio_exportacao.mkdir(parents=True, exist_ok=True)
    configuracao.arquivo_log.parent.mkdir(parents=True, exist_ok=True)
    return configuracao
