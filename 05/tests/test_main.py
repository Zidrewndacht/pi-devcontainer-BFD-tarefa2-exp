import json
import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import main
from config import Configuracao


class TestMain(unittest.TestCase):
    def test_cria_aplicacao_e_banco(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            capitais = raiz / "capitais.json"
            capitais.write_text(
                json.dumps(
                    {
                        "PR": {
                            "capital": "Curitiba",
                            "latitude": -25.4284,
                            "longitude": -49.2733,
                        }
                    }
                ),
                encoding="utf-8",
            )
            configuracao = Configuracao(
                ibge_url="https://exemplo.test/{uf}",
                nominatim_domain="exemplo.test",
                user_agent="trabalho-teste",
                timeout=5,
                intervalo_requisicoes=1.1,
                uf_padrao="PR",
                banco=raiz / "municipios.db",
                arquivo_capitais=capitais,
                diretorio_exportacao=raiz / "exports",
                arquivo_log=raiz / "aplicacao.log",
            )
            with (
                patch("main.carregar_configuracao", return_value=configuracao),
                patch("main.configurar_logging"),
            ):
                aplicacao = main.criar_aplicacao()
            self.assertTrue(configuracao.banco.is_file())
            self.assertEqual(aplicacao.configuracao.uf_padrao, "PR")

    def test_ctrl_c_encerra_sem_erro(self) -> None:
        aplicacao = Mock()
        aplicacao.executar.side_effect = KeyboardInterrupt
        console = Mock()
        with (
            patch("main.criar_aplicacao", return_value=aplicacao),
            patch("main.Console", return_value=console),
        ):
            main.main()
        console.print.assert_called_once()

    def test_execucao_como_script(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            raiz = Path(pasta)
            capitais = raiz / "capitais.json"
            capitais.write_text(
                '{"PR":{"capital":"Curitiba","latitude":-25.4,"longitude":-49.2}}',
                encoding="utf-8",
            )
            configuracao = Configuracao(
                ibge_url="https://exemplo.test/{uf}",
                nominatim_domain="exemplo.test",
                user_agent="trabalho-teste",
                timeout=5,
                intervalo_requisicoes=1.1,
                uf_padrao="",
                banco=raiz / "municipios.db",
                arquivo_capitais=capitais,
                diretorio_exportacao=raiz / "exports",
                arquivo_log=raiz / "aplicacao.log",
            )
            with (
                patch("config.carregar_configuracao", return_value=configuracao),
                patch("logging_config.configurar_logging"),
                patch("interface.InterfaceTerminal.executar"),
            ):
                runpy.run_path(Path(main.__file__), run_name="__main__")


if __name__ == "__main__":
    unittest.main()
