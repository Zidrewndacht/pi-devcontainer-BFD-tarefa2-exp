import logging
from pathlib import Path

from servicos import ServicoMunicipios


def processar_arquivo(caminho: Path, servico: ServicoMunicipios) -> dict[str, object]:
    if not caminho.is_file():
        raise FileNotFoundError("O arquivo informado não foi encontrado.")
    resultado: dict[str, object] = {"total": 0, "sucessos": [], "falhas": []}
    with caminho.open(encoding="utf-8-sig") as entrada:
        for numero, linha in enumerate(entrada, start=1):
            conteudo = linha.strip()
            if not conteudo or conteudo.startswith("#"):
                continue
            resultado["total"] = int(resultado["total"]) + 1
            partes = [parte.strip() for parte in conteudo.split(";")]
            if len(partes) != 2:
                resultado["falhas"].append(
                    {"linha": numero, "entrada": conteudo, "erro": "formato inválido"}
                )
                continue
            nome, uf = partes
            try:
                municipio = servico.obter_municipio(nome, uf)
                resultado["sucessos"].append(municipio)
            except (ValueError, RuntimeError) as erro:
                logging.warning("Falha no batch, linha %s: %s", numero, erro)
                resultado["falhas"].append(
                    {"linha": numero, "entrada": conteudo, "erro": str(erro)}
                )
    return resultado
