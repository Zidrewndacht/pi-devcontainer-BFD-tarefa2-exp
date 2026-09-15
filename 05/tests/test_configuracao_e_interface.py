import json
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from rich.console import Console

from config import Configuracao, carregar_configuracao
from dashboard import montar_dashboard
from database import BancoDados
from interface import InterfaceTerminal
from logging_config import configurar_logging
from models import Municipio


class TestConfiguracaoEInterface(unittest.TestCase):
    def setUp(self) -> None:
        self.pasta = tempfile.TemporaryDirectory()
        raiz = Path(self.pasta.name)
        self.configuracao = Configuracao(
            ibge_url="https://exemplo.test/{uf}",
            nominatim_domain="exemplo.test",
            user_agent="trabalho-teste",
            timeout=5,
            intervalo_requisicoes=1.1,
            uf_padrao="PR",
            banco=raiz / "municipios.db",
            arquivo_capitais=raiz / "capitais.json",
            diretorio_exportacao=raiz / "exports",
            arquivo_log=raiz / "aplicacao.log",
        )
        self.banco = BancoDados(self.configuracao.banco)
        self.banco.criar_estrutura()
        self.servico = Mock()
        self.console = Console(record=True, width=120, file=io.StringIO())
        self.interface = InterfaceTerminal(
            self.servico, self.banco, self.configuracao, self.console
        )
        self.municipio = Municipio(
            4106902,
            "Curitiba",
            "PR",
            -25.4284,
            -49.2733,
            "2026-01-01T10:00:00-03:00",
        )

    def tearDown(self) -> None:
        self.pasta.cleanup()

    def test_carrega_json_e_variaveis_de_ambiente(self) -> None:
        raiz = Path(self.pasta.name)
        arquivo = raiz / "config.json"
        dados = {
            "ibge_url": "https://exemplo.test/{uf}",
            "nominatim_domain": "exemplo.test",
            "user_agent": "teste",
            "timeout": 10,
            "intervalo_requisicoes": 1.1,
            "uf_padrao": "pr",
            "banco": str(raiz / "dados" / "teste.db"),
            "arquivo_capitais": str(raiz / "capitais.json"),
            "diretorio_exportacao": str(raiz / "exports"),
            "arquivo_log": str(raiz / "logs" / "teste.log"),
        }
        arquivo.write_text(json.dumps(dados), encoding="utf-8")
        with patch.dict("os.environ", {"TAREFA5_TIMEOUT": "30"}):
            configuracao = carregar_configuracao(arquivo)
        self.assertEqual(configuracao.timeout, 30)
        self.assertEqual(configuracao.uf_padrao, "PR")
        self.assertTrue(configuracao.banco.parent.is_dir())
        self.assertTrue(configuracao.diretorio_exportacao.is_dir())

    def test_menu_pode_ser_encerrado(self) -> None:
        with patch("interface.Prompt.ask", return_value="0"):
            self.interface.executar()
        self.assertIn("Aplicação encerrada", self.console.export_text())

    def test_busca_e_distancia_sao_exibidas(self) -> None:
        self.servico.obter_municipio.return_value = self.municipio
        with patch.object(
            self.interface, "_pedir_municipio", return_value=("Curitiba", "PR")
        ):
            self.interface.buscar()
        destino = Municipio(
            3550308,
            "São Paulo",
            "SP",
            -23.5505,
            -46.6333,
            "2026-01-01T10:00:00-03:00",
        )
        self.servico.calcular_distancia.return_value = {
            "origem": self.municipio,
            "destino": destino,
            "quilometros": 338.4,
            "milhas": 210.3,
            "vizinhos": False,
            "aproximada": False,
        }
        with patch.object(
            self.interface,
            "_pedir_municipio",
            side_effect=[("Curitiba", "PR"), ("São Paulo", "SP")],
        ):
            self.interface.calcular_distancia()
        texto = self.console.export_text()
        self.assertIn("Curitiba", texto)
        self.assertIn("338.40 km", texto)
        self.assertIn("Não são vizinhos", texto)

    def test_sincronizacao_e_proximos_sao_exibidos(self) -> None:
        resultado = {
            "total": 2,
            "sucessos": 1,
            "cache": 1,
            "aproximados": 0,
            "falhas": 0,
            "medias": (-24.0, -50.0),
            "estimativa_segundos": 1.1,
            "duracao_segundos": 1.2,
        }

        def sincronizar(uf: str, atualizar: object) -> dict[str, object]:
            atualizar(1, 2, "Curitiba")
            return resultado

        self.servico.sincronizar.side_effect = sincronizar
        with patch.object(self.interface, "_pedir_uf", return_value="PR"):
            self.interface.sincronizar()
        self.servico.municipios_proximos.return_value = [
            {"municipio": self.municipio, "distancia": 12.5}
        ]
        with (
            patch.object(
                self.interface, "_pedir_municipio", return_value=("Londrina", "PR")
            ),
            patch("interface.Prompt.ask", return_value="20"),
        ):
            self.interface.listar_proximos()
        texto = self.console.export_text()
        self.assertIn("Resumo da sincronização", texto)
        self.assertIn("12.50 km", texto)

        self.servico.sincronizar.side_effect = None
        self.servico.sincronizar.return_value = {**resultado, "medias": None}
        with patch.object(self.interface, "_pedir_uf", return_value="PR"):
            self.interface.sincronizar()
        self.servico.municipios_proximos.return_value = []
        with (
            patch.object(
                self.interface, "_pedir_municipio", return_value=("Londrina", "PR")
            ),
            patch("interface.Prompt.ask", return_value="1"),
        ):
            self.interface.listar_proximos()
        self.assertIn("Nenhum município sincronizado", self.console.export_text())

    def test_listagem_mapa_dashboard_e_configuracoes(self) -> None:
        self.banco.salvar_municipio(self.municipio)
        with patch("interface.Confirm.ask", return_value=False):
            self.interface.listar_sincronizados()
        with patch.object(self.interface, "_pedir_uf", return_value="PR"):
            self.interface.mapa_ascii()
        self.interface.dashboard()
        self.interface.exibir_configuracoes()
        texto = self.console.export_text()
        self.assertIn("Municípios sincronizados", texto)
        self.assertIn("Mapa ASCII", texto)
        self.assertIn("PAINEL DE ESTATÍSTICAS", texto)
        self.assertIn("Configurações em uso", texto)

    def test_exportacao_e_batch_pela_interface(self) -> None:
        self.banco.salvar_municipio(self.municipio)
        self.configuracao.diretorio_exportacao.mkdir(exist_ok=True)
        with (
            patch("interface.Prompt.ask", return_value="csv"),
            patch("interface.Confirm.ask", return_value=False),
        ):
            self.interface.exportar()
        arquivos = list(self.configuracao.diretorio_exportacao.glob("*.csv"))
        self.assertEqual(len(arquivos), 1)
        with (
            patch("interface.Prompt.ask", return_value="json"),
            patch("interface.Confirm.ask", return_value=True),
            patch.object(self.interface, "_pedir_uf", return_value="PR"),
        ):
            self.interface.exportar()
        self.assertEqual(
            len(list(self.configuracao.diretorio_exportacao.glob("*.json"))), 1
        )
        entrada = Path(self.pasta.name) / "entrada.txt"
        entrada.write_text("Curitiba;PR\n", encoding="utf-8")
        self.servico.obter_municipio.return_value = self.municipio
        with patch("interface.Prompt.ask", return_value=str(entrada)):
            self.interface.processar_batch()
        self.assertIn("Resultado do processamento", self.console.export_text())

        entrada.write_text("linha inválida\n", encoding="utf-8")
        with patch("interface.Prompt.ask", return_value=str(entrada)):
            self.interface.processar_batch()
        self.assertIn("formato inválido", self.console.export_text())

    def test_menu_trata_erro_da_operacao(self) -> None:
        with (
            self.assertLogs(level="ERROR"),
            patch("interface.Prompt.ask", side_effect=["2", "", "0"]),
            patch.object(
                self.interface, "buscar", side_effect=ValueError("entrada inválida")
            ),
        ):
            self.interface.executar()
        self.assertIn("Não foi possível concluir", self.console.export_text())

    def test_dashboard_vazio_e_formatacao_de_tempo(self) -> None:
        layout = montar_dashboard(self.banco.estatisticas())
        self.console.print(layout)
        self.assertIn("Municípios", self.console.export_text())
        self.assertEqual(self.interface._formatar_tempo(3661), "1 h 1 min 1 s")

    def test_listagem_e_mapa_sem_dados(self) -> None:
        self.interface._exibir_tabela_municipios([], "Teste")
        with self.assertRaises(ValueError):
            with patch.object(self.interface, "_pedir_uf", return_value="PR"):
                self.interface.mapa_ascii()
        self.assertIn("Nenhum município sincronizado", self.console.export_text())
        with (
            patch("interface.Prompt.ask", return_value="csv"),
            patch("interface.Confirm.ask", return_value=False),
            self.assertRaises(ValueError),
        ):
            self.interface.exportar()

    def test_prompts_e_filtro_por_uf(self) -> None:
        self.banco.salvar_municipio(self.municipio)
        with patch("interface.Prompt.ask", side_effect=["pr", "Curitiba", "pr"]):
            self.assertEqual(self.interface._pedir_uf(), "PR")
            self.assertEqual(self.interface._pedir_municipio(), ("Curitiba", "PR"))
        with (
            patch("interface.Confirm.ask", return_value=True),
            patch.object(self.interface, "_pedir_uf", return_value="PR"),
        ):
            self.interface.listar_sincronizados()

    def test_configuracao_do_log(self) -> None:
        with patch("logging.basicConfig") as basic_config:
            configurar_logging(self.configuracao.arquivo_log)
        basic_config.assert_called_once()
        manipulador = basic_config.call_args.kwargs["handlers"][0]
        manipulador.close()


if __name__ == "__main__":
    unittest.main()
