import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from models import Municipio
from validacoes import normalizar_nome


class BancoDados:
    def __init__(self, caminho: Path):
        self.caminho = caminho

    @contextmanager
    def conectar(self) -> Iterator[sqlite3.Connection]:
        conexao = sqlite3.connect(self.caminho)
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        try:
            yield conexao
            conexao.commit()
        except Exception:
            conexao.rollback()
            raise
        finally:
            conexao.close()

    def criar_estrutura(self) -> None:
        with self.conectar() as conexao:
            conexao.executescript(
                """
                CREATE TABLE IF NOT EXISTS municipios (
                    id_ibge INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    nome_normalizado TEXT NOT NULL,
                    uf TEXT NOT NULL CHECK(length(uf) = 2),
                    latitude REAL NOT NULL CHECK(latitude BETWEEN -90 AND 90),
                    longitude REAL NOT NULL CHECK(longitude BETWEEN -180 AND 180),
                    data_consulta TEXT NOT NULL,
                    fonte_coordenada TEXT NOT NULL,
                    coordenada_aproximada INTEGER NOT NULL DEFAULT 0,
                    endereco_retornado TEXT NOT NULL DEFAULT ''
                );
                CREATE INDEX IF NOT EXISTS idx_municipios_uf ON municipios(uf);
                CREATE INDEX IF NOT EXISTS idx_municipios_busca
                    ON municipios(uf, nome_normalizado);
                CREATE TABLE IF NOT EXISTS sincronizacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    uf TEXT NOT NULL,
                    inicio TEXT NOT NULL,
                    termino TEXT NOT NULL,
                    total INTEGER NOT NULL,
                    sucessos INTEGER NOT NULL,
                    cache INTEGER NOT NULL,
                    aproximados INTEGER NOT NULL,
                    falhas INTEGER NOT NULL,
                    duracao_segundos REAL NOT NULL
                );
                """
            )

    def salvar_municipio(self, municipio: Municipio) -> None:
        with self.conectar() as conexao:
            conexao.execute(
                """
                INSERT INTO municipios (
                    id_ibge, nome, nome_normalizado, uf, latitude, longitude,
                    data_consulta, fonte_coordenada, coordenada_aproximada,
                    endereco_retornado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id_ibge) DO UPDATE SET
                    nome = excluded.nome,
                    nome_normalizado = excluded.nome_normalizado,
                    uf = excluded.uf,
                    latitude = excluded.latitude,
                    longitude = excluded.longitude,
                    data_consulta = excluded.data_consulta,
                    fonte_coordenada = excluded.fonte_coordenada,
                    coordenada_aproximada = excluded.coordenada_aproximada,
                    endereco_retornado = excluded.endereco_retornado
                """,
                (
                    municipio.id_ibge,
                    municipio.nome,
                    normalizar_nome(municipio.nome),
                    municipio.uf,
                    municipio.latitude,
                    municipio.longitude,
                    municipio.data_consulta,
                    municipio.fonte_coordenada,
                    int(municipio.coordenada_aproximada),
                    municipio.endereco_retornado,
                ),
            )

    def buscar_municipio(self, nome: str, uf: str) -> Municipio | None:
        with self.conectar() as conexao:
            linha = conexao.execute(
                """
                SELECT * FROM municipios
                WHERE nome_normalizado = ? AND uf = ?
                """,
                (normalizar_nome(nome), uf),
            ).fetchone()
        return self._converter(linha) if linha else None

    def buscar_por_id(self, id_ibge: int) -> Municipio | None:
        with self.conectar() as conexao:
            linha = conexao.execute(
                "SELECT * FROM municipios WHERE id_ibge = ?", (id_ibge,)
            ).fetchone()
        return self._converter(linha) if linha else None

    def listar_municipios(self, uf: str | None = None) -> list[Municipio]:
        consulta = "SELECT * FROM municipios"
        parametros: tuple[str, ...] = ()
        if uf:
            consulta += " WHERE uf = ?"
            parametros = (uf,)
        consulta += " ORDER BY uf, nome COLLATE NOCASE"
        with self.conectar() as conexao:
            linhas = conexao.execute(consulta, parametros).fetchall()
        return [self._converter(linha) for linha in linhas]

    def registrar_sincronizacao(self, dados: dict[str, object]) -> None:
        campos = (
            "uf",
            "inicio",
            "termino",
            "total",
            "sucessos",
            "cache",
            "aproximados",
            "falhas",
            "duracao_segundos",
        )
        with self.conectar() as conexao:
            conexao.execute(
                f"INSERT INTO sincronizacoes ({', '.join(campos)}) VALUES ({', '.join('?' for _ in campos)})",
                tuple(dados[campo] for campo in campos),
            )

    def estatisticas(self) -> dict[str, object]:
        with self.conectar() as conexao:
            totais = conexao.execute(
                """
                SELECT COUNT(*) AS total,
                       COUNT(DISTINCT uf) AS ufs,
                       SUM(coordenada_aproximada) AS aproximados,
                       MAX(data_consulta) AS ultima_consulta
                FROM municipios
                """
            ).fetchone()
            distribuicao = conexao.execute(
                "SELECT uf, COUNT(*) AS quantidade FROM municipios GROUP BY uf ORDER BY uf"
            ).fetchall()
            fontes = conexao.execute(
                "SELECT fonte_coordenada, COUNT(*) AS quantidade FROM municipios GROUP BY fonte_coordenada"
            ).fetchall()
            ultima_sincronizacao = conexao.execute(
                "SELECT * FROM sincronizacoes ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return {
            "total": totais["total"],
            "ufs": totais["ufs"],
            "aproximados": totais["aproximados"] or 0,
            "ultima_consulta": totais["ultima_consulta"],
            "distribuicao": [dict(linha) for linha in distribuicao],
            "fontes": [dict(linha) for linha in fontes],
            "ultima_sincronizacao": dict(ultima_sincronizacao)
            if ultima_sincronizacao
            else None,
        }

    @staticmethod
    def medias(municipios: Iterable[Municipio]) -> tuple[float, float] | None:
        itens = list(municipios)
        if not itens:
            return None
        return (
            sum(item.latitude for item in itens) / len(itens),
            sum(item.longitude for item in itens) / len(itens),
        )

    @staticmethod
    def _converter(linha: sqlite3.Row) -> Municipio:
        return Municipio(
            id_ibge=linha["id_ibge"],
            nome=linha["nome"],
            uf=linha["uf"],
            latitude=linha["latitude"],
            longitude=linha["longitude"],
            data_consulta=linha["data_consulta"],
            fonte_coordenada=linha["fonte_coordenada"],
            coordenada_aproximada=bool(linha["coordenada_aproximada"]),
            endereco_retornado=linha["endereco_retornado"],
        )
