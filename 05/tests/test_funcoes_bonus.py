import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from batch import processar_arquivo
from exportacao import exportar_csv, exportar_json
from mapa_ascii import gerar_mapa
from models import Municipio
from validacoes import normalizar_nome, validar_nome, validar_raio, validar_uf


class TestFuncoesBonus(unittest.TestCase):
    def setUp(self) -> None:
        self.municipios = [
            Municipio(1, "Curitiba", "PR", -25.42, -49.27, "2026-01-01"),
            Municipio(2, "Londrina", "PR", -23.31, -51.16, "2026-01-01"),
        ]

    def test_normalizacoes_e_validacoes(self) -> None:
        self.assertEqual(normalizar_nome("  São   José  "), "sao jose")
        self.assertEqual(validar_uf(" pr "), "PR")
        self.assertEqual(validar_raio("12,5"), 12.5)
        with self.assertRaises(ValueError):
            validar_uf("XX")
        with self.assertRaises(ValueError):
            validar_raio("texto")
        with self.assertRaises(ValueError):
            validar_raio("0")
        with self.assertRaises(ValueError):
            validar_nome("1")

    def test_mapa_ascii(self) -> None:
        mapa = gerar_mapa(self.municipios, largura=20, altura=8)
        self.assertIn("* município", mapa)
        self.assertIn("Latitude", mapa)
        with self.assertRaises(ValueError):
            gerar_mapa([])

    def test_exportacoes(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            diretorio = Path(pasta)
            csv = exportar_csv(self.municipios, diretorio)
            json_arquivo = exportar_json(self.municipios, diretorio)
            self.assertIn("Curitiba", csv.read_text(encoding="utf-8-sig"))
            dados = json.loads(json_arquivo.read_text(encoding="utf-8"))
            self.assertEqual(dados[1]["nome"], "Londrina")

    def test_processamento_em_lote(self) -> None:
        servico = Mock()
        servico.obter_municipio.side_effect = [
            self.municipios[0],
            ValueError("município inválido"),
        ]
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "entrada.txt"
            arquivo.write_text(
                "# exemplo\nCuritiba;PR\nlinha sem separador\nInexistente;PR\n",
                encoding="utf-8",
            )
            with self.assertLogs(level="WARNING"):
                resultado = processar_arquivo(arquivo, servico)
        self.assertEqual(resultado["total"], 3)
        self.assertEqual(len(resultado["sucessos"]), 1)
        self.assertEqual(len(resultado["falhas"]), 2)

    def test_batch_rejeita_arquivo_inexistente(self) -> None:
        with self.assertRaises(FileNotFoundError):
            processar_arquivo(Path("arquivo-que-nao-existe.txt"), Mock())


if __name__ == "__main__":
    unittest.main()
