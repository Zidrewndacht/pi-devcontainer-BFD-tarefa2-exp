import tempfile
import unittest
from pathlib import Path

from database import BancoDados
from models import Municipio


class TestBancoDados(unittest.TestCase):
    def setUp(self) -> None:
        self.pasta = tempfile.TemporaryDirectory()
        self.banco = BancoDados(Path(self.pasta.name) / "teste.db")
        self.banco.criar_estrutura()

    def tearDown(self) -> None:
        self.pasta.cleanup()

    def test_salva_busca_e_atualiza_sem_duplicar(self) -> None:
        municipio = Municipio(
            4106902, "Curitiba", "PR", -25.4284, -49.2733, "2026-01-01T10:00:00-03:00"
        )
        self.banco.salvar_municipio(municipio)
        atualizado = Municipio(
            4106902, "Curitiba", "PR", -25.43, -49.27, "2026-01-02T10:00:00-03:00"
        )
        self.banco.salvar_municipio(atualizado)
        encontrado = self.banco.buscar_municipio("curítiba", "PR")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.id_ibge, 4106902)
        self.assertAlmostEqual(encontrado.latitude, -25.43)
        self.assertEqual(len(self.banco.listar_municipios()), 1)

    def test_estatisticas_do_banco_vazio(self) -> None:
        estatisticas = self.banco.estatisticas()
        self.assertEqual(estatisticas["total"], 0)
        self.assertEqual(estatisticas["aproximados"], 0)
        self.assertIsNone(self.banco.medias([]))

    def test_conexao_reverte_transacao_com_erro(self) -> None:
        with self.assertRaises(RuntimeError):
            with self.banco.conectar() as conexao:
                conexao.execute(
                    """
                    INSERT INTO sincronizacoes (
                        uf, inicio, termino, total, sucessos, cache,
                        aproximados, falhas, duracao_segundos
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    ("PR", "inicio", "fim", 1, 1, 0, 0, 0, 1.0),
                )
                raise RuntimeError("erro simulado")
        with self.banco.conectar() as conexao:
            total = conexao.execute("SELECT COUNT(*) FROM sincronizacoes").fetchone()[0]
        self.assertEqual(total, 0)


if __name__ == "__main__":
    unittest.main()
