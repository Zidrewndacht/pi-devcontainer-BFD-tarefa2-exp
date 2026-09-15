import logging

import requests

from validacoes import normalizar_nome


class ErroIBGE(RuntimeError):
    pass


class ClienteIBGE:
    def __init__(self, url: str, timeout: int):
        self.url = url
        self.timeout = timeout

    def listar_municipios(self, uf: str) -> list[dict[str, int | str]]:
        endereco = self.url.format(uf=uf)
        logging.info("Consulta ao IBGE para a UF %s", uf)
        try:
            resposta = requests.get(endereco, timeout=self.timeout)
            resposta.raise_for_status()
            conteudo = resposta.json()
        except (requests.RequestException, ValueError) as erro:
            logging.exception("Falha ao consultar o IBGE para %s", uf)
            raise ErroIBGE(
                "Não foi possível consultar os municípios no IBGE."
            ) from erro
        if not isinstance(conteudo, list):
            raise ErroIBGE("O IBGE retornou dados em um formato inesperado.")
        municipios: list[dict[str, int | str]] = []
        for item in conteudo:
            if (
                isinstance(item, dict)
                and isinstance(item.get("id"), int)
                and isinstance(item.get("nome"), str)
            ):
                municipios.append({"id": item["id"], "nome": item["nome"], "uf": uf})
        if not municipios:
            raise ErroIBGE("Nenhum município foi retornado para a UF informada.")
        return municipios

    def encontrar_municipio(self, nome: str, uf: str) -> dict[str, int | str] | None:
        procurado = normalizar_nome(nome)
        return next(
            (
                item
                for item in self.listar_municipios(uf)
                if normalizar_nome(str(item["nome"])) == procurado
            ),
            None,
        )
