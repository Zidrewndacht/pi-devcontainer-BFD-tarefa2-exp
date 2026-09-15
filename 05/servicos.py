import json
import logging
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from time import perf_counter

from database import BancoDados
from geocodificador import (
    Geocodificador,
    LocalizacaoNaoEncontrada,
    ServicoGeocodificacaoIndisponivel,
)
from ibge_api import ClienteIBGE
from models import Municipio
from validacoes import validar_nome, validar_uf


Atualizador = Callable[[int, int, str], None]


class ServicoMunicipios:
    def __init__(
        self,
        banco: BancoDados,
        ibge: ClienteIBGE,
        geocodificador: Geocodificador,
        arquivo_capitais: Path,
        intervalo: float,
    ):
        self.banco = banco
        self.ibge = ibge
        self.geocodificador = geocodificador
        self.intervalo = intervalo
        with arquivo_capitais.open(encoding="utf-8") as entrada:
            self.capitais: dict[str, dict[str, float | str]] = json.load(entrada)

    @staticmethod
    def agora() -> str:
        return datetime.now().astimezone().isoformat(timespec="seconds")

    def sincronizar(
        self, uf: str, atualizar: Atualizador | None = None
    ) -> dict[str, object]:
        sigla = validar_uf(uf)
        inicio_texto = self.agora()
        inicio = perf_counter()
        itens = self.ibge.listar_municipios(sigla)
        pendentes = [
            item
            for item in itens
            if not (existente := self.banco.buscar_por_id(int(item["id"])))
            or existente.coordenada_aproximada
        ]
        resultado: dict[str, object] = {
            "uf": sigla,
            "inicio": inicio_texto,
            "total": len(itens),
            "estimativa_segundos": len(pendentes) * self.intervalo,
            "sucessos": 0,
            "cache": len(itens) - len(pendentes),
            "aproximados": 0,
            "falhas": 0,
        }
        for indice, item in enumerate(itens, start=1):
            nome = str(item["nome"])
            existente = self.banco.buscar_por_id(int(item["id"]))
            if existente and not existente.coordenada_aproximada:
                if atualizar:
                    atualizar(indice, len(itens), f"{nome} (cache)")
                continue
            try:
                municipio = self._geocodificar(int(item["id"]), nome, sigla)
                self.banco.salvar_municipio(municipio)
                resultado["sucessos"] = int(resultado["sucessos"]) + 1
            except ServicoGeocodificacaoIndisponivel:
                municipio = self._usar_capital(int(item["id"]), nome, sigla)
                self.banco.salvar_municipio(municipio)
                resultado["aproximados"] = int(resultado["aproximados"]) + 1
            except LocalizacaoNaoEncontrada:
                resultado["falhas"] = int(resultado["falhas"]) + 1
                logging.warning("Sem coordenadas para %s/%s", nome, sigla)
            if atualizar:
                atualizar(indice, len(itens), nome)
        termino = self.agora()
        duracao = perf_counter() - inicio
        resultado["termino"] = termino
        resultado["duracao_segundos"] = duracao
        armazenados = self.banco.listar_municipios(sigla)
        resultado["medias"] = self.banco.medias(armazenados)
        self.banco.registrar_sincronizacao(resultado)
        logging.info("Sincronização de %s finalizada: %s", sigla, resultado)
        return resultado

    def obter_municipio(self, nome: str, uf: str) -> Municipio:
        nome_validado = validar_nome(nome)
        sigla = validar_uf(uf)
        existente = self.banco.buscar_municipio(nome_validado, sigla)
        if existente:
            return existente
        item = self.ibge.encontrar_municipio(nome_validado, sigla)
        if item is None:
            raise LocalizacaoNaoEncontrada(
                f"{nome_validado} não consta na lista do IBGE para {sigla}."
            )
        try:
            municipio = self._geocodificar(int(item["id"]), str(item["nome"]), sigla)
        except ServicoGeocodificacaoIndisponivel:
            municipio = self._usar_capital(int(item["id"]), str(item["nome"]), sigla)
        self.banco.salvar_municipio(municipio)
        return municipio

    def calcular_distancia(
        self,
        nome_origem: str,
        uf_origem: str,
        nome_destino: str,
        uf_destino: str,
    ) -> dict[str, object]:
        origem = self.obter_municipio(nome_origem, uf_origem)
        destino = self.obter_municipio(nome_destino, uf_destino)
        quilometros, milhas = self.geocodificador.distancia(origem, destino)
        return {
            "origem": origem,
            "destino": destino,
            "quilometros": quilometros,
            "milhas": milhas,
            "vizinhos": quilometros < 50,
            "aproximada": origem.coordenada_aproximada or destino.coordenada_aproximada,
        }

    def municipios_proximos(
        self, nome: str, uf: str, raio: float
    ) -> list[dict[str, object]]:
        origem = self.obter_municipio(nome, uf)
        encontrados: list[dict[str, object]] = []
        for municipio in self.banco.listar_municipios():
            if municipio.id_ibge == origem.id_ibge:
                continue
            quilometros, _ = self.geocodificador.distancia(origem, municipio)
            if quilometros <= raio:
                encontrados.append({"municipio": municipio, "distancia": quilometros})
        encontrados.sort(key=lambda item: float(item["distancia"]))
        return encontrados

    def _geocodificar(self, id_ibge: int, nome: str, uf: str) -> Municipio:
        local = self.geocodificador.geocodificar(nome, uf)
        return Municipio(
            id_ibge=id_ibge,
            nome=nome,
            uf=uf,
            latitude=local.latitude,
            longitude=local.longitude,
            data_consulta=self.agora(),
            endereco_retornado=local.endereco,
        )

    def _usar_capital(self, id_ibge: int, nome: str, uf: str) -> Municipio:
        capital = self.capitais[uf]
        logging.warning("Fallback da capital usado para %s/%s", nome, uf)
        return Municipio(
            id_ibge=id_ibge,
            nome=nome,
            uf=uf,
            latitude=float(capital["latitude"]),
            longitude=float(capital["longitude"]),
            data_consulta=self.agora(),
            fonte_coordenada="capital_fallback",
            coordenada_aproximada=True,
            endereco_retornado=f"Coordenada aproximada de {capital['capital']}",
        )
